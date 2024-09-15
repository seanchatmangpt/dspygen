from datetime import datetime

from dspygen.pyautomator.base_app import BaseApp


class KeynoteApp(BaseApp):
    def __init__(self):
        super().__init__("Keynote")

    def create_presentation(self, save_to_file: bool = False):
        script = """
        const keynote = Application('Keynote');
        keynote.includeStandardAdditions = true;
        const presentation = keynote.Document().make();
        keynote.documents.push(presentation);
        """
        return self.execute_jxa(script, save_to_file=save_to_file)

    def add_slide(self, layout="Title & Subtitle", save_to_file: bool = False):
        script = f"""
        const keynote = Application('Keynote');
        const presentation = keynote.documents[0]; // Target the first open presentation
        const slide = presentation.slides.push(keynote.Slide({{ baseSlide: presentation.masterSlides['{layout}'] }}));
        """
        return self.execute_jxa(script, save_to_file=save_to_file)

    def add_text_to_slide(self, slide_index=0, text="Your Text Here", size=24, x=100, y=100, save_to_file: bool = False):
        script = f"""
        const keynote = Application('Keynote');
        const presentation = keynote.documents[0]; // Assume the first open presentation
        const slide = presentation.slides[{slide_index}];
        const textItem = slide.defaultTitleItem();
        textItem.objectText = '{text}';
        textItem.textSize = {size};
        textItem.position = {{x: {x}, y: {y}}};
        """
        return self.execute_jxa(script, save_to_file=save_to_file)

    def insert_image(self, slide_index=0, image_path="", x=200, y=200, width=300, height=200, save_to_file: bool = False):
        script = f"""
        const keynote = Application('Keynote');
        const presentation = keynote.documents[0];
        const slide = presentation.slides[{slide_index}];
        const image = slide.images.push(keynote.Image({{
            file: Path('{image_path}'),
            position: {{x: {x}, y: {y}}},
            width: {width},
            height: {height}
        }}));
        """
        return self.execute_jxa(script, save_to_file=save_to_file)

    def add_animation(self, slide_index=0, object_index=0, animation_type='move', duration=2, save_to_file: bool = False):
        script = f"""
        const keynote = Application('Keynote');
        const presentation = keynote.documents[0];
        const slide = presentation.slides[{slide_index}];
        const item = slide.slideItems[{object_index}];
        item.animations.push(keynote.Build({{
            type: '{animation_type}',
            duration: {duration}
        }}));
        """
        return self.execute_jxa(script, save_to_file=save_to_file)

    def export_to_pdf(self, file_path, save_to_file: bool = False):
        script = f"""
        const keynote = Application('Keynote');
        const presentation = keynote.documents[0];
        presentation.export({{
            to: Path('{file_path}'),
            as: 'PDF'
        }});
        """
        return self.execute_jxa(script, save_to_file=save_to_file)

    def start_slideshow(self, save_to_file: bool = False):
        script = """
        const keynote = Application('Keynote');
        const presentation = keynote.documents[0];
        presentation.startSlideshow();
        """
        return self.execute_jxa(script, save_to_file=save_to_file)
