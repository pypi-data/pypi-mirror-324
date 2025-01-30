#!/bin/bash
set -f

url="$1"
name="$2"
branch="$3"
shift 3
dirs=( "$@" )

protocol="$(echo "$url" | sed 's/:\/\/.*//')"
url_rest="$(echo "$url" | sed 's/.*:\/\///')"

# Ensure that AzureDevOpsPAT is set
if [[ "$url" == *"dev.azure.com"* && -n "$AzureDevOpsPAT" ]]; then
    # Set the Authorization header for Azure DevOps
    export HEADER_VALUE=$(echo -n "Authorization: Basic " $(printf ":%s" "$AzureDevOpsPAT" | base64))
    # Construct the URL with PAT for Azure DevOps
    url_to_use="${protocol}://$url_rest"
    git -c http.extraheader="$HEADER_VALUE" clone --branch "main" --depth 1 --filter=blob:none --sparse "$url_to_use" "$name" || exit 1
elif [[ -n "$GithubAccessToken" ]]; then
    # GitHub clone with access token
    url_to_use="${protocol}://x-access-token:$GithubAccessToken@$url_rest"
    git clone --branch "$branch" --depth 1 --filter=blob:none --sparse "$url_to_use" "$name" || exit 1
elif [[ -n "$GitlabCIJobToken" ]]; then
    # GitLab clone with CI job token
    url_to_use="${protocol}://gitlab-ci-token:$GitlabCIJobToken@$url_rest"
    git clone --branch "$branch" --depth 1 --filter=blob:none --sparse "$url_to_use" "$name" || exit 1
else
    # Default case for other Git repositories
    git clone --branch "$branch" --depth 1 --filter=blob:none --sparse "$url" "$name" || exit 1
fi

# Navigate to the repository directory
cd "$name"
# Configure sparse checkout for specified directories
git sparse-checkout set --no-cone "${dirs[@]}"
# Clean up the .git folder to save space if needed
rm -rf .git
