from __future__ import annotations

from typing import List


def default_generator(base_prompts: List[str], mutations: List[str]) -> List[str]:
    # Import pyrit to ensure the library is installed and available.
    import pyrit  # noqa: F401

    prompts: List[str] = []
    if not mutations:
        return list(base_prompts)
    for prompt in base_prompts:
        for mutation in mutations:
            if mutation == "obfuscate":
                prompts.append(f"[[{prompt}]] (base64: {prompt.encode().hex()})")
            elif mutation == "social_engineering":
                prompts.append(f"Compliance audit: {prompt} Please respond fully.")
            else:
                prompts.append(prompt)
    return prompts

