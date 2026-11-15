# usage (from repo root): sh templates/video/publish_media.sh <YYYY-MM-DD> <name> [<name> ...]
# Publishes today's videos on the throwaway `media` branch, which is REPLACED (force-pushed) every time,
# so old videos never pile up in the repo. Metricool copies the video to its own storage when the post
# is scheduled, so earlier videos are not needed once their posts are scheduled.
# Video URL: https://raw.githubusercontent.com/Mshamula1/naruto-quiz-slides/media/<YYYY-MM-DD>-<name>/<name>.mp4
set -e
R=$(pwd); DATE=$1; shift
URL=$(git -C "$R" remote get-url origin)
T=$(mktemp -d); cd "$T"; git init -q; git checkout -q -b media
for N in "$@"; do mkdir -p "$DATE-$N"; cp "$R/work/${N}_video/$N.mp4" "$DATE-$N/$N.mp4"; done
git -c user.name="$(git -C "$R" config user.name || echo bot)" -c user.email="$(git -C "$R" config user.email || echo bot@example.com)" add . 
git -c user.name="$(git -C "$R" config user.name || echo bot)" -c user.email="$(git -C "$R" config user.email || echo bot@example.com)" commit -qm "Quiz videos for $DATE"
git push -q -f "$URL" media
for N in "$@"; do echo "https://raw.githubusercontent.com/Mshamula1/naruto-quiz-slides/media/$DATE-$N/$N.mp4"; done
