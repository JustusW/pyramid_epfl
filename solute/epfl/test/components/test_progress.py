import pytest
from solute.epfl import components

def test_render_progress_bar(page):
    page.root_node = components.Progress(
                                         min=10,
                                         value=20,
                                         max=30
    )
    page.handle_transaction()

    compo = page.root_node
    assert 'class="progress-bar' in compo.render(), "progress-bar class not found"
    assert 'aria-valuemin="10"' in compo.render(), "min value not found"
    assert 'aria-valuenow="20"' in compo.render(), "min value not found"
    assert 'aria-valuemax="30"' in compo.render(), "min value not found"

def test_render_stacked_progress_bar(page):
    page.root_node = components.StackedProgress(
                                         value=[(10, 'progress-bar-info'), (50, 'progress-bar-success')]
    )
    page.handle_transaction()

    compo = page.root_node
    assert 'class="progress-bar progress-bar-info" style="width: 10%"' in compo.render(), "first progress bar not found"
    assert 'class="progress-bar progress-bar-success" style="width: 50%"' in compo.render(), "first progress bar not found"
