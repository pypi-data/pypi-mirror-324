# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test `commition.plugin.pdm` module."""

from __future__ import annotations

import pathlib
import shutil
import tempfile
import uuid

import git

import hypothesis
import pytest

import commition


@hypothesis.strategies.composite
def repository(
    draw: hypothesis.strategies.DrawFn, *, n_commits: int = 10
) -> git.Repo:
    """Create repository with `n_commits` commits.

    Commits will have the same text, but different scope,
    all are changing the same file over and over.

    Args:
        draw:
            Hypothesis draw function.
        n_commits:
            Number of commits to create.

    Returns:
        Repository with `n_commits` commits.
    """
    directory = pathlib.Path(tempfile.mkdtemp())
    repo = git.Repo.init(directory)
    file = directory / "file.txt"

    version = pytest.CommitionVersionTester()

    for _ in range(n_commits):
        commit_type = draw(
            hypothesis.strategies.sampled_from(["fix", "feat", "feat!", "fix!"])
        )
        with file.open("w") as f:
            f.write(str(uuid.uuid4()))

        repo.index.add(file)
        repo.index.commit(
            f"{commit_type}: bla bla bla",
            author=git.Actor("Alice", "alice@example.com"),
        )

        version.bump(commit_type)

    return repo, commition.Version.from_numbers(*version.to_tuple())


# @pytest.mark.parametrize("path_include", (None,))
# @pytest.mark.parametrize("path_exclude", (None,))
@pytest.mark.parametrize("path_include", (None, (".*", "a")))
@pytest.mark.parametrize("path_exclude", (None, (".*", "b")))
@pytest.mark.parametrize("author_name_include", (None, (".*", "Alice")))
@pytest.mark.parametrize("author_name_exclude", (None, (".*", "Bob")))
@pytest.mark.parametrize("author_email_include", (None, (".*", ".*@gmail.com")))
@pytest.mark.parametrize(
    "author_email_exclude", (None, (".*", ".*@example.com"))
)
@hypothesis.settings(max_examples=1)
@hypothesis.given(repository=repository())
def test_pdm(  # noqa: PLR0913
    path_include: tuple[str] | None,
    path_exclude: tuple[str] | None,
    author_name_include: tuple[str] | None,
    author_name_exclude: tuple[str] | None,
    author_email_include: tuple[str] | None,
    author_email_exclude: tuple[str] | None,
    repository: tuple[git.Repo, commition.Version],
) -> None:
    """Test `commition.plugin.pdm.git` function.

    Tests if `commition.plugin.pdm.git` function returns
    correct version and whether regex based filtering works.

    See `commition.plugin.pdm.git` docs for more details.

    Args:
        path_include:
            Regular expression for included path.
        path_exclude:
            Regular expression for excluded path.
        author_name_include:
            Regular expression for included author name.
        author_name_exclude:
            Regular expression for excluded author name.
        author_email_include:
            Regular expression for included author email.
        author_email_exclude:
            Regular expression for excluded author email.
        repository:
            Repository with commits.
    """
    repository, test_version = repository
    commition_version = commition.Version.from_string(
        commition.plugin.pdm.git(
            repository=repository,
            path_include=path_include,
            path_exclude=path_exclude,
            author_name_include=author_name_include,
            author_name_exclude=author_name_exclude,
            author_email_include=author_email_include,
            author_email_exclude=author_email_exclude,
        )
    )

    if author_name_exclude or author_email_exclude:
        assert commition_version == commition.Version.from_numbers(0, 0, 0)
    # In case of path_exclude, we will get either 0.1.0, 1.0.0 or 0.0.1
    elif path_exclude:
        assert commition_version in (
            commition.Version.from_numbers(0, 1, 0),
            commition.Version.from_numbers(1, 0, 0),
            commition.Version.from_numbers(0, 0, 1),
        )
    else:
        assert commition_version == test_version

    shutil.rmtree(repository.working_dir)


def test_smoke_current_repo() -> None:
    """Test `commition.plugin.pdm.git` function on current repository.

    This is a smoke test to check if `commition.plugin.pdm.git`
    function works on current repository.

    Parsing commits from this project is complex and requires the samek work
    as the library itself, so we only check if the function runs without
    errors.

    """
    commition.plugin.pdm.git()
