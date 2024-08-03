from confz import BaseConfig, FileSource
from typing import List, Optional
from pydantic import BaseModel


class Chapter(BaseModel):
    title: str
    path: Optional[str] = None
    subchapters: List['Chapter'] = []


class SummaryConfig(BaseConfig):
    title: Optional[str]
    prefix_chapters: List[Chapter] = []
    numbered_chapters: List[Chapter] = []
    suffix_chapters: List[Chapter] = []

    CONFIG_SOURCES = FileSource(file='summary_config.yaml')


# Example to convert the config to SUMMARY.md format
def generate_summary_md(config: SummaryConfig) -> str:
    lines = []

    if config.title:
        lines.append(f"# {config.title}\n")

    for chapter in config.prefix_chapters:
        lines.append(f"[{chapter.title}]({chapter.path})\n")

    def process_chapters(chapters, indent=0):
        lines = []
        for chapter in chapters:
            prefix = "    " * indent + "- "
            lines.append(f"{prefix}[{chapter.title}]({chapter.path})\n")
            lines.extend(process_chapters(chapter.subchapters, indent + 1))
        return lines

    lines.extend(process_chapters(config.numbered_chapters))

    for chapter in config.suffix_chapters:
        lines.append(f"[{chapter.title}]({chapter.path})\n")

    return ''.join(lines)


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    config = SummaryConfig()
    print(config)

    summary_md_content = generate_summary_md(config)
    print(summary_md_content)


if __name__ == '__main__':
    main()
