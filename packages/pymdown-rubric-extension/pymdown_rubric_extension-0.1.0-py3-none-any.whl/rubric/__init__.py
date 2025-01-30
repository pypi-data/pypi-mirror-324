import xml.etree.ElementTree as etree

import yaml
from pymdownx.blocks import BlocksExtension
from pymdownx.blocks.block import Block, type_html_identifier

__version__ = "0.1.0"


class Rubric(Block):
    """Figure captions."""

    NAME = 'rubric'
    ARGUMENT = None
    OPTIONS = {'type': ['', type_html_identifier]}

    def __init__(self, length, tracker, md, config):
        """Initialize."""

        self.classes = config['classes']
        if type(self.classes) is list:
            self.classes = ' '.join(self.classes)

        super().__init__(length, tracker, md, config)

    def on_markdown(self):
        return "raw"

    def on_create(self, parent):
        """Initialize."""

        el = etree.SubElement(parent, 'table')
        if self.classes:
            el.set('class', self.classes)

        return el

    def on_end(self, block):
        """Finalize."""
        self.parse_rubric(block.text)
        block.text = ""

        self.handle_levels(block)
        self.handle_criteria(block)

        return block

    def parse_rubric(self, text):
        """Parse rubric."""

        self.data = yaml.safe_load(text)

    def handle_levels(self, block):
        thead = etree.SubElement(block, 'thead')
        tr = etree.SubElement(thead, 'tr')
        th = etree.SubElement(tr, 'th')
        for level in self.data['levels']:
            th = etree.SubElement(tr, 'th')
            self.handle_level(th, level)

    def handle_level(self, block, level):
        if type(level) is str:
            title = level
            score = None
        else:
            title = level['title']
            score = level.get('score')

        title_el = etree.SubElement(block, 'div', {'class': 'rubric__level-title'})
        title_el.text = title
        if score:
            score_el = etree.SubElement(block, 'div', {'class': 'rubric__level-score'})
            score_el.text = score

    def handle_criteria(self, block):
        tbody = etree.SubElement(block, 'tbody')
        for criterion in self.data['criteria']:
            tr = etree.SubElement(tbody, 'tr')
            td = etree.SubElement(tr, 'td')
            title = etree.SubElement(td, 'div', {'class': 'rubric__criteria-title'})
            title.text = criterion['title']

            if 'description' in criterion:
                description = etree.SubElement(td, 'div', {'class': 'rubric__criteria-description'})
                description.text = criterion['description']
            if 'score' in criterion:
                score = etree.SubElement(td, 'div', {'class': 'rubric__criteria-score'})
                score.text = criterion['score']

            for level in criterion['levels']:
                self.handle_criterion_level(tr, level)

    def handle_criterion_level(self, block, level):
        if type(level) is str:
            title = level
            score = None
            checked = False
        else:
            title = level['title']
            score = level.get('score')
            checked = level.get('checked', False)

        classes = 'rubric__criteria-element'
        if checked:
            classes += ' checked'

        td = etree.SubElement(block, 'td', {'class': classes})
        title_el = etree.SubElement(td, 'div', {'class': 'rubric__criteria-element-description'})
        title_el.text = title
        if score:
            score_el = etree.SubElement(td, 'div', {'class': 'rubric__criteria-element-score'})
            score_el.text = score


class RubricExtension(BlocksExtension):
    """Rubric Extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {'classes': ['', 'Classes to add to the rubric table - Default: ""']}

        super().__init__(*args, **kwargs)

    def extendMarkdownBlocks(self, md, block_mgr):
        """Extend Markdown blocks."""

        config = self.getConfigs()
        block_mgr.register(Rubric, config)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return RubricExtension(*args, **kwargs)
