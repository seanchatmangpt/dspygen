from pydantic import BaseModel, Field
from typing import List, Optional

import re
import yaml
from datetime import datetime

from dspygen.modules.file_name_module import file_name_call
from sungen.utils.dspy_tools import predict_type


class Link(BaseModel):
    target_note_id: str = Field(..., description="The ID of the target note being linked to.")
    description: Optional[str] = Field(None, description="An optional description of the link.")

class Tag(BaseModel):
    name: str = Field(..., description="The name of the tag.")

class Note(BaseModel):
    id: str = Field(..., description="Unique identifier for the note.")
    title: str = Field(..., description="The title of the note.")
    content: str = Field(..., description="The main content of the note.")
    tags: List[Tag] = Field([], description="A list of tags associated with the note.")
    aliases: List[str] = Field([], description="Alternate names for the note.")
    cssclass: str = Field("", description="CSS class for styling the note in Obsidian.")
    links: List[Link] = Field([], description="A list of links pointing to other notes.")
    created_at: datetime = Field(..., description="The datetime when the note was created.")
    updated_at: datetime = Field(..., description="The datetime when the note was last updated.")
    publish: bool = Field(False, description="Whether or not the note is published.")
    permalink: str = Field("", description="The permalink or URL for the note.")
    description: str = Field("", description="A short description of the note.")
    image: str = Field("", description="URL or path to an image associated with the note.")
    cover: str = Field("", description="URL or path to a cover image associated with the note.")


def to_obsidian_md(note: Note) -> str:
    # Prepare YAML frontmatter
    frontmatter = {
        "id": note.id,
        "title": note.title,
        "aliases": note.aliases,
        "cssclass": note.cssclass,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
        "publish": note.publish,
        "permalink": note.permalink,
        "description": note.description,
        "image": note.image,
        "cover": note.cover,
        # "tags": note.tags,
        # "links": [{"target_note_id": link['target_note_id'], "description": link['description']} for link in note.links]
    }

    # Convert frontmatter to YAML format
    yaml_frontmatter = yaml.dump(frontmatter, sort_keys=False)

    # Add YAML delimiters for Obsidian frontmatter
    md_string = f"---\n{yaml_frontmatter}---\n\n"

    # Add the main content
    md_string += f"# {note.title}\n\n{note.content}\n\n"

    # Add tags at the bottom of the note
    # if note.tags:
    #     md_string += ' '.join([f"#{tag}" for tag in note.tags]) + "\n"

    # Add links at the bottom of the note
    # if note.links:
    #     for link in note.links:
    #         md_string += f"[{link['description']}]({link['target_note_id']})\n"

    return md_string


def from_obsidian_md(md_str: str) -> Note:
    # Regular expression pattern to extract the YAML frontmatter and the body
    pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)', re.S)
    match = pattern.match(md_str)

    if not match:
        raise ValueError("The input markdown string is not in the correct Obsidian format.")

    # Extract YAML frontmatter and body content
    yaml_part, content_part = match.groups()

    # Parse the YAML frontmatter
    frontmatter = yaml.safe_load(yaml_part)

    # Convert the frontmatter dictionary to a Note object
    note = Note(
        id=frontmatter.get('id', ''),
        title=frontmatter.get('title', ''),
        content=content_part.strip(),
        tags=frontmatter.get('tags', []),
        aliases=frontmatter.get('aliases', []),
        cssclass=frontmatter.get('cssclass', ''),
        # links=frontmatter.get('links', []),
        created_at=datetime.fromisoformat(frontmatter.get('created_at', datetime.now().isoformat())),
        updated_at=datetime.fromisoformat(frontmatter.get('updated_at', datetime.now().isoformat())),
        publish=frontmatter.get('publish', False),
        permalink=frontmatter.get('permalink', ''),
        description=frontmatter.get('description', ''),
        image=frontmatter.get('image', ''),
        cover=frontmatter.get('cover', '')
    )

    return note


def to_obsidian_md_file(note: Note, file_path: str="") -> None:
    md_str = to_obsidian_md(note)
    with open(file_path, 'w') as file:
        file.write(md_str)


def from_obsidian_md_file(file_path: str="") -> Note:
    with open(file_path, 'r') as file:
        md_str = file.read()
    return from_obsidian_md(md_str)


def main2():
    """Main function"""
    from sungen.utils.dspy_tools import init_dspy
    init_dspy()

    res = predict_type({"text": text}, Note)
    print(res)

    to_obsidian_md_file(res, file_name_call(text))


def main():
    """Main function"""
    file_path = "/dspygen/experiments/obsidian_gen/2024-07-15_Power_and_Prediction_ML_and_Grid_Dynamics.md"
    note = from_obsidian_md_file(file_path)
    print(note) 


if __name__ == '__main__':
    main()
