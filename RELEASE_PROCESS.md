# How to Create a New Release for Your Python Package

This guide provides step-by-step instructions for creating a new release for your Python package using GitHub Actions. The process involves updating the changelog, version in `setup.py`, and pushing a new tag to trigger the automated workflow.

## Step 1: Update `CHANGELOG.md`

Ensure your `CHANGELOG.md` has an entry for the new version you are about to release. For example:

\`\`\`markdown

# Changelog

## v0.5.0

- New release
- Added feature X

## v0.4.0

- Improved feature X
- Fixed bug Y
  \`\`\`

## Step 2: Update `setup.py`

Update the `version` field in your `setup.py` to match the new version:

## Step 3: Commit and Push Changes

Commit your changes to `CHANGELOG.md` and `setup.py`.

## Step 4: Create and Push a Tag

1. **Create a New Tag**:

   \`\`\`bash
   git tag v0.5.0
   \`\`\`

2. **Push the Tag to the Remote Repository**:

   \`\`\`bash
   git push origin v0.5.0
   \`\`\`

## What Happens Next

### GitHub Actions Workflow

The following GitHub Actions workflow (`publish.yml`) will be triggered by the new tag. This workflow handles the extraction of version and release notes, updates the `README_PyPi.md`, builds the package, publishes it to PyPI, and creates a GitHub release.

### Verification

After pushing the tag, you can verify that the tag has been created and pushed successfully by checking your GitHub repository:

1. **Go to your repository on GitHub**.
2. **Click on the "Tags" link** to see the list of tags.
3. **Check the Actions tab** to see the running workflows triggered by the new tag.

This streamlined process ensures that your new release is properly documented, built, published, and released on both PyPI and GitHub.
