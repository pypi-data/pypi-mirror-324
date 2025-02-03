# 🧠 blue-assistant

🧠 `@assistant` is an AI assistant.

```bash
pip install blue-assistant
```

```mermaid
graph LR
    assistant_script_list["@assistant<br>script<br>list"]
    assistant_script_run["@assistant<br>script<br>run -<br>&lt;script&gt;<br>&lt;object-name&gt;"]

    script["📜 script"]:::folder
    object["📂 object"]:::folder

    script --> assistant_script_list

    script --> assistant_script_run
    object --> assistant_script_run
    assistant_script_run --> object

    classDef folder fill:#999,stroke:#333,stroke-width:2px;
```

---


[![pylint](https://github.com/kamangir/blue-assistant/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/blue-assistant/actions/workflows/pylint.yml) [![pytest](https://github.com/kamangir/blue-assistant/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/blue-assistant/actions/workflows/pytest.yml) [![bashtest](https://github.com/kamangir/blue-assistant/actions/workflows/bashtest.yml/badge.svg)](https://github.com/kamangir/blue-assistant/actions/workflows/bashtest.yml) [![PyPI version](https://img.shields.io/pypi/v/blue-assistant.svg)](https://pypi.org/project/blue-assistant/) [![PyPI - Downloads](https://img.shields.io/pypi/dd/blue-assistant)](https://pypistats.org/packages/blue-assistant)

built by 🌀 [`blue_options-4.207.1`](https://github.com/kamangir/awesome-bash-cli), based on 🧠 [`blue_assistant-4.53.1`](https://github.com/kamangir/blue-assistant).
