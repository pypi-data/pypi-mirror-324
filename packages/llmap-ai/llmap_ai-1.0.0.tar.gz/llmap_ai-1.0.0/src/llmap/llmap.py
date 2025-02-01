import argparse
import os
import random
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, TypeVar

from tqdm import tqdm

from .ai import AI, collate, SourceAnalysis
from .exceptions import AIException
from .parse import chunk, parseable_extension

T = TypeVar('T')

# we're using an old tree-sitter API
import warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='tree_sitter')


def search(question: str, source_files: list[str], llm_concurrency: int = 200, refine: bool = True, analyze_skeletons: bool = True) -> tuple[list[AIException], str]:
    """
    Search source files for relevance to a question.
    
    Args:
        question: The question to analyze relevance against
        source_files: List of source file paths to analyze
        llm_concurrency: Maximum number of concurrent LLM requests
        refine: Whether to refine and combine analyses
        
    Returns:
        tuple[list[AIException], str]: A tuple containing:
            - List of non-fatal AIException errors encountered during processing
            - Formatted string containing the analysis results
    """
    # Create AI client and thread pool
    client = AI()

    def process_phase(
        executor: ThreadPoolExecutor,
        items: list[T],
        process_fn: Callable[[T], T],
        desc: str,
        client: AI
    ) -> tuple[list[T], list[AIException]]:
        """
        Process a batch of items with progress tracking and error handling.
        
        Args:
            executor: Thread pool executor
            items: List of items to process
            process_fn: Function to process each item
            desc: Description for progress bar
            client: AI client for progress tracking
            
        Returns:
            tuple of (results, errors) where:
            - results is a list of successfully processed items
            - errors is a list of AIException errors encountered
        """
        results = []
        errors = []
        tqdm_postfix = {"Rcvd": 0}
        futures = [executor.submit(process_fn, item) for item in items]

        with tqdm(total=len(futures), desc=desc,
                 bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}{postfix}') as pbar:
            def cb(n_lines):
                tqdm_postfix['Rcvd'] += n_lines
                pbar.set_postfix(tqdm_postfix)
            client.progress_callback = cb

            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except AIException as e:
                    errors.append(e)
                pbar.update(1)
                
        return results, errors

    # Create thread pool and process files
    errors = []
    relevant_files = []
    with ThreadPoolExecutor(max_workers=llm_concurrency) as executor:
        # Split files by whether we can parse a skeleton (unless disabled)
        if not analyze_skeletons:
            parseable_files = set()
        else:
            parseable_files = {f for f in source_files if parseable_extension(f)}
        other_files = [f for f in source_files if f not in parseable_files]

        # Phase 1: Generate initial relevance against skeletons for parseable files
        if parseable_files:
            skeleton_results, phase1_errors = process_phase(
                executor,
                parseable_files,
                lambda f: client.skeleton_relevance(f, question),
                "Skeleton analysis",
                client
            )
            
            # Process results and collect relevant files
            for file_path, analysis in skeleton_results:
                if 'LLMAP_RELEVANT' in analysis:
                    relevant_files.append(file_path)
            errors.extend(phase1_errors)

        # Add non-parseable files directly to relevant_files for full source analysis
        relevant_files.extend(other_files)

        # Phase 2: extract and analyze source code chunks from relevant files
        # First get all chunks
        file_chunks, phase2a_errors = process_phase(
            executor,
            relevant_files,
            lambda f: (f, chunk(f)),
            "Parsing full source",
            client
        )
        errors.extend(phase2a_errors)

        # Flatten chunks into (file_path, chunk_text) pairs for analysis
        chunk_pairs = []
        for file_path, chunks in file_chunks:
            if chunks:
                for chunk_text in chunks:
                    chunk_pairs.append((file_path, chunk_text))

        # Analyze all chunks
        chunk_analyses, phase2b_errors = process_phase(
            executor,
            chunk_pairs,
            lambda pair: client.full_source_relevance(pair[1], question, pair[0]),
            "Analyzing full source",
            client
        )
        errors.extend(phase2b_errors)

        # Group analyses by file and combine
        analyses_by_file = defaultdict(list)
        for (file_path, analysis) in chunk_analyses:
            analyses_by_file[file_path].append(analysis)

        # sorted so the caching is deterministic
        chunk_results = sorted(SourceAnalysis(file_path, "\n\n".join(sorted(analyses)))
                               for file_path, analyses in analyses_by_file.items())

        # Collate and process results
        groups, large_files = collate(chunk_results)

        # Refine groups in parallel
        if refine:
            processed_contexts, phase4_errors = process_phase(
                executor,
                groups,
                lambda g: client.sift_context(g, question),
                "Refining analysis",
                client
            )
            errors.extend(phase4_errors)
        else:
            # If no refinement, just flatten the groups into individual results
            processed_contexts = [f'File{file_path}\n{analysis}\n\n'
                                  for group in groups for file_path, analysis in group]

    # Build output string
    output = ""
    for context in processed_contexts:
        if context:
            output += f"{context}\n\n"
    for file_path, analysis in large_files:
        output += f"{file_path}:\n{analysis}\n\n"
        
    return errors, output


def main():
    parser = argparse.ArgumentParser(description='Analyze source files for relevance to a question')
    parser.add_argument('question', help='Question to check relevance against')
    parser.add_argument('--sample', type=int, help='Number of random files to sample from the input set')
    parser.add_argument('--llm-concurrency', type=int, default=200, help='Maximum number of concurrent LLM requests')
    parser.add_argument('--no-refine', action='store_false', dest='refine', help='Skip refinement and combination of analyses')
    parser.add_argument('--no-skeletons', action='store_false', dest='analyze_skeletons', help='Skip skeleton analysis phase for all files')
    args = parser.parse_args()

    # Read files from stdin
    source_files = []
    for line in sys.stdin:
        file_path = line.strip()
        if not os.path.isfile(file_path):
            print(f"Warning: File does not exist: {file_path}", file=sys.stderr)
            continue
        source_files.append(file_path)

    if not source_files:
        print("Error: No valid source files provided", file=sys.stderr)
        return 1

    # Sample files if requested
    if args.sample and args.sample < len(source_files):
        source_files = random.sample(source_files, args.sample)

    errors, result = search(args.question, source_files, args.llm_concurrency, args.refine, args.analyze_skeletons)
    if errors:
        print("Errors encountered:", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        print(file=sys.stderr)
    print(result)
        

if __name__ == "__main__":
    main()
