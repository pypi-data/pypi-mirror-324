#!/bin/bash
set -f

url="$1"
docs_dir="$2"
branch=$3
AzureDevOpsPAT="$4"
shift 3
dirs=( "$@" )


mkdir -p "$docs_dir" # make the section directory
cd "$docs_dir"
# initialize git
git init

protocol="$(echo "$url" | sed 's/:\/\/.*//')"
url_rest="$(echo "$url" | sed 's/.*:\/\///')"

if [[ "$url" == *"dev.azure.com"* && -n "$AzureDevOpsPAT" ]]; then
    # Set the Authorization header for Azure DevOps
    export HEADER_VALUE=$(echo -n "Authorization: Basic " $(printf ":%s" "$AzureDevOpsPAT" | base64))
    # Construct the URL with PAT for Azure DevOps
    echo $AzureDevOpsPAT
    echo $HEADER_VALUE
    url_to_use="${protocol}://$url_rest"
    git -c http.extraheader="$HEADER_VALUE" clone --branch "main" --depth 1 --filter=blob:none --sparse "$url_to_use" "$name" || exit 1
elif [[ -n  "$AccessToken" ]]; then
    url_to_use="${protocol}://$AccessToken@$url_rest"
    git config http.extraheader "AUTHORIZATION: bearer $AccessToken"
elif [[ -n  "$GithubAccessToken" ]]; then
    url_to_use="${protocol}://x-access-token:$GithubAccessToken@$url_rest"
elif [[ -n  "$GitlabCIJobToken" ]]; then
    url_to_use="${protocol}://gitlab-ci-token:$GitlabCIJobToken@$url_rest"
else
  url_to_use="$url"
fi
# sparse checkout the old way
git config core.sparseCheckout true
git remote add -f origin "$url_to_use"
# .git/info might not exist after git init, depending on git version
# (e.g. git 2.24.1 does not create it)
mkdir -p .git/info
for dir in "${dirs[@]}"
do
   printf "${dir}\n">> .git/info/sparse-checkout
done
git checkout $branch
rm -rf .git
