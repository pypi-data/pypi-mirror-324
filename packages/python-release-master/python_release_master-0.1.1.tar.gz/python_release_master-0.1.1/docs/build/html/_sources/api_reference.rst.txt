API Reference
=============

This section provides detailed documentation for the Python Release Master API.

AI Module
--------

.. py:module:: python_release_master.core.ai

.. py:function:: generate_changelog_with_ai(sections: List[str], model: str = "gpt-4-0125-preview") -> Dict[str, Any]

   Generate a changelog using OpenAI with structured output.

   :param sections: List of section names to organize changes (e.g., ["Features", "Bug Fixes"])
   :param model: OpenAI model to use (default: "gpt-4-0125-preview")
   :return: Dictionary containing changelog data with the following structure:

   .. code-block:: python

      {
          "version_bump": "major|minor|patch",
          "bump_reason": "explanation of why this bump type was chosen",
          "changes": [
              {
                  "title": "commit/PR title",
                  "description": "detailed description",
                  "section": "one of the available sections",
                  "type": "feat|fix|docs|style|refactor|test|chore",
                  "breaking": boolean
              }
          ],
          "changelog_md": "final markdown formatted changelog with sections"
      }

.. py:function:: commit_changes_with_ai() -> Optional[str]

   Generate commit message and commit changes using AI.

   :return: The generated commit message if changes were committed, None otherwise.

.. py:function:: get_commits_since_last_tag() -> List[str]

   Get all commit messages since the last tag.

   :return: List of commit messages with their hashes.

.. py:function:: get_pull_requests_since_last_tag() -> List[dict]

   Get all merged pull requests since the last tag.

   :return: List of pull request data dictionaries.

Release Module
------------

.. py:module:: python_release_master.core.release

.. py:function:: create_release(bump_type: str, title: str, description: Optional[str], config: Config, skip_steps: Optional[List[str]] = None) -> None

   Create a new release.

   :param bump_type: Type of version bump ("major", "minor", "patch")
   :param title: Release title
   :param description: Optional release description
   :param config: Release configuration
   :param skip_steps: Optional list of steps to skip

.. py:function:: bump_version(bump_type: str, version_files: List[str]) -> None

   Bump version in all specified files.

   :param bump_type: Type of version bump ("major", "minor", "patch")
   :param version_files: List of files containing version strings

Configuration
-----------

.. py:module:: python_release_master.core.config

.. py:class:: Config

   Main configuration for Python Release Master.

   .. py:attribute:: version_files
      :type: List[str]

      List of files containing version strings.

   .. py:attribute:: changelog
      :type: ChangelogConfig

      Configuration for changelog generation.

   .. py:attribute:: skip_steps
      :type: List[str]

      List of steps to skip during release.

.. py:class:: ChangelogConfig

   Configuration for changelog generation.

   .. py:attribute:: ai_powered
      :type: bool

      Whether to use AI-powered changelog generation.

   .. py:attribute:: openai_model
      :type: str

      OpenAI model to use for generation.

   .. py:attribute:: sections
      :type: List[str]

      List of sections to organize changes. 