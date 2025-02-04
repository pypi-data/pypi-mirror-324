"""Module with helper functions to easily parse ollama options from a string
as well as dump available options and/or their description to a string."""

import re

# Jan 2025. Weird pylint bug, see https://github.com/pylint-dev/pylint/issues/10112
from collections.abc import Iterable  # pylint: disable = E0401
from textwrap import fill as twfill
from typing import Any, get_type_hints

from ollama import Options as oOptions

# get names of options + types directly from Ollama
OLLAMA_OPTION_TYPES = get_type_hints(oOptions)

# paranoia check ... should never happen except if Ollama library changes drastically
#
if len(OLLAMA_OPTION_TYPES) == 0:
    raise RuntimeError(
        "Something seems to have drastically changed in the Ollama Python library:"
        " typehints of Ollama options has length 0. Sorry, need to abort."
    )  # pragma: nocover


# Descriptions for Ollama options. Would be nice if one could get that interactively
#  from the server, but ... well, that's second best possibility.
#
# taken from https://pypi.org/project/ollama-python/
# ... which had more complete description
# than https://github.com/ollama/ollama/blob/main/docs/modelfile.md :-(((
OLLAMA_OPTION_DESC = {
    "mirostat": (
        "Enable Mirostat sampling for controlling perplexity. (default: 0, 0 = disabled,"
        " 1 = Mirostat, 2 = Mirostat 2.0)"
    ),
    "mirostat_eta": (
        "Influences how quickly the algorithm responds to feedback from the generated text."
        " A lower learning rate will result in slower adjustments, while a higher learning"
        " rate will make the algorithm more responsive. (Default: 0.1)"
    ),
    "mirostat_tau": (
        "Controls the balance between coherence and diversity of the output. A lower value"
        " will result in more focused and coherent text. (Default: 5.0)"
    ),
    "num_ctx": ("Sets the size of the context window used to generate the next token. (Default: 2048)"),
    "num_gqa": (
        "The number of GQA groups in the transformer layer. Required for some models, for example"
        "it is 8 for llama2:70b"
    ),
    "num_gpu": (
        "The number of layers to send to the GPU(s). On macOS it defaults to 1 to enable metal"
        " support, 0 to disable."
    ),
    "num_thread": (
        "Sets the number of threads to use during computation. By default, Ollama will detect"
        " this for optimal performance. It is recommended to set this value to the number of"
        " physical CPU cores your system has (as opposed to the logical number of cores)."
    ),
    "repeat_last_n": (
        "Sets how far back for the model to look back to prevent repetition. (Default: 64,"
        " 0 = disabled, -1 = num_ctx)"
    ),
    "repeat_penalty": (
        "Sets how strongly to penalize repetitions. A higher value (e.g., 1.5) will"
        " penalize repetitions more strongly, while a lower value (e.g., 0.9) will be more"
        " lenient. (Default: 1.1)"
    ),
    "temperature": (
        "The temperature of the model. Increasing the temperature will make the model answer"
        " more creatively. (Default: 0.8)"
    ),
    "seed": (
        "Sets the random number seed to use for generation. Setting this to a specific number will"
        " make the model generate the same text for the same prompt. (Default: 0)"
    ),
    "stop": (
        "Sets the stop sequences to use. When this pattern is encountered the LLM will stop generating"
        " text and return. Multiple stop patterns may be set by specifying multiple separate stop"
        " options in a modelfile."
    ),
    "tfs_z": (
        "Tail free sampling is used to reduce the impact of less probable tokens from the output."
        " A higher value (e.g., 2.0) will reduce the impact more, while a value of 1.0 disables"
        " this setting. (default: 1)"
    ),
    "num_predict": (
        "Maximum number of tokens to predict when generating text. (Default: 128,"
        " -1 = infinite generation, -2 = fill context)"
    ),
    "top_k": (
        "Reduces the probability of generating nonsense. A higher value (e.g. 100) will give more"
        " diverse answers, while a lower value (e.g. 10) will be more conservative. (Default: 40)"
    ),
    "top_p": (
        "Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text,"
        " while a lower value (e.g., 0.5) will generate more focused and conservative text."
        " (Default: 0.9)"
    ),
}


def help_overview() -> str:
    """Convenience. Create a string showing name and type of supported Ollama options."""

    collection = _collect_ollama_options()
    max_namelen = len(max(collection, key=lambda x: len(x[0]))[0]) + 3

    mtext = "(multiple)"
    tlist: list[str] = []
    for pname, ptype, multiple in collection:
        ms = "" if not multiple else mtext
        tlist.append(f"{pname:>{max_namelen}} : {ptype:<6} {ms}")
    return "\n".join(tlist)


def help_long() -> str:
    """Convenience. Create a string showing name, type and description of supported Ollama
    options.
    Note: The description text for options is not present in the Ollama Python module,
    some options even have no good description online at all.
    """
    collection = _collect_ollama_options()
    tlist: list[str] = []
    mtext = "(multiple)"
    for pname, ptype, multiple in collection:
        ms = "" if not multiple else mtext
        tlist.append(f"{pname} : {ptype} {ms}")
        if pname in OLLAMA_OPTION_DESC:
            tlist.append(twfill(OLLAMA_OPTION_DESC[pname]))
        else:
            tlist.append(
                "This parameter seems to be new, or not described in docs as of"
                " January 2025.\ndm_ollamalib does not know it, sorry."
            )
        tlist.append("")
    return "\n".join(tlist)


def _collect_ollama_options() -> list[tuple[str, str, bool]]:
    collection: list[tuple[str, str, bool]] = []
    for pname, ptype in OLLAMA_OPTION_TYPES.items():
        match = re.search(r"\[(.*?)\]$", str(ptype))
        multiple = False
        if match:
            ptype = match.group(1)  # noqa: PLW2901
            match = re.search(r"\[(.*?)\]$", ptype)
            if match:
                ptype = match.group(1)  # noqa: PLW2901
                multiple = True
        collection.append((pname, ptype, multiple))
    return collection


def to_ollama_options(options: str | Iterable[str]) -> dict[str, Any]:
    """Transform a string (or an Iterable of strings) with semicolon separated Ollama options to dict.

    The Python Ollama library wants the Ollama options as correct Python types in a dict,
    i.e., one cannot use strings. This functions transforms any string with
    Ollama options into a dict with correct types.
    Ollama uses a TypedDict, the dict[str, Any] returned by this function is compatible.

    Arguments:
    - options: Either str or Iterable[str]. E.g. "num_ctx=8092;temperature=0.8"

    Exceptions raised:
    - ValueError for
        - unrecognised Ollama options
        - conversion errors of a string to required type (int, float, bool)
        - incomplete options (e.g. "num_ctx=" or "=8092")
        - unknown Ollama options
    - RuntimeError if Ollama Python library has unexpected parameter types not handled
      by this function (should not happen, except if Ollama devs implemented something new)
    """

    if isinstance(options, str):
        return _string_to_ollama_options(options)
    if isinstance(options, Iterable):
        retval: dict[str, Any] = {}
        for p in options:
            retval |= _string_to_ollama_options(p)
        return retval
    raise TypeError("'options' is neither a str nor an Iterable")


# ruff complains about too many branches
# ... that's life when checking validity of user input
#
def _string_to_ollama_options(params: str) -> dict[str, Any]:  # noqa: PLR0912
    """Internal _string_to_ollama_params for just str type"""

    def _check_pname_pval(pn, pv):
        """Factored out as inner function to circumvent pylint R0912 (too many branches)"""
        if len(pn) == 0:
            raise ValueError("Ollama parameter (left of equal sign) is empty")
        if len(pv) == 0:
            raise ValueError(f"Ollama parameter '{pn}' is empty (nothing right of equal sign)")
        if pn not in OLLAMA_OPTION_TYPES:
            known = ", ".join(sorted(OLLAMA_OPTION_TYPES.keys()))
            raise ValueError(f"Unknown ollama parameter '{pn}'. Known options:\n{known}")

    # if I were to use ollama.Options as type, pylint would throw errors
    #  down below for lines like
    #     oparams[pname] = pval
    # Therefore, we'll use this ... Ollama will be fine
    oparams: dict[str, Any] = {}

    for semsplit in params.split(";"):
        plist = [x.strip() for x in semsplit.split("=")]

        # Check syntactic validity of this parameter:
        # there must be an equal sign and a left and a right side.

        if len(plist) == 1 and len(plist[0]) == 0:
            continue  # no = sign but empty string ... let that pass
        if len(plist) < 2:  # noqa: PLR2004
            raise ValueError(f"Missing an equal sign ('=') in '{semsplit}'")
        if len(plist) > 2:  # noqa: PLR2004
            raise ValueError(f"Found more than one equal sign ('=') in '{semsplit}'")

        pname, pval = plist
        _check_pname_pval(pname, pval)

        # Argh! match cannot directly match types.
        # Going via the string representation is ... ugly

        ptype = str(OLLAMA_OPTION_TYPES[pname])
        match ptype:
            case "typing.Optional[int]":
                try:
                    oparams[pname] = int(pval)
                except ValueError as e:
                    raise ValueError(
                        f"Ollama parameter '{pname}' expected an int, got '{{pval}}'\n{{e}}"
                    ) from e
            case "typing.Optional[float]":
                try:
                    oparams[pname] = float(pval)
                except ValueError as e:
                    raise ValueError(f"Ollama parameter '{pname}' expected a float, got '{pval}'") from e
            case "typing.Optional[bool]":
                pval = pval.lower()
                if pval == "false":
                    oparams[pname] = False
                elif pval == "true":
                    oparams[pname] = True
                else:
                    raise ValueError(f"Ollama parameter '{pname}' expected 'true' or 'false', got '{pval}'")
            case "typing.Optional[typing.Sequence[str]]":
                if pname in oparams:
                    oparams[pname].append(str(pval))
                else:
                    oparams[pname] = [str(pval)]
            case "typing.Optional[str]":  # pragma: nocover
                # currently not used by the Ollama Python module, but easy to be prepared
                oparams[pname] = str(pval)
            case _:  # pragma: nocover
                raise RuntimeError(
                    "Type Ollama uses not yet handled!"
                    f" Parameter type '{OLLAMA_OPTION_TYPES[pname]}' for '{pname}'."
                )
    return oparams
