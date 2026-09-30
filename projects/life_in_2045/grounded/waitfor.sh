# usage: bash waitfor.sh <name-glob> [max_minutes]  -- waits for ComfyUI output video H3_<glob>_0*.mp4
for i in $(seq 1 $(( ${2:-40} * 6 ))); do ls /d/Projects_26/Comfyu/ComfyUI/output/video/H3_$1_0*.mp4 >/dev/null 2>&1 && { echo ready $1; exit 0; }; sleep 10; done; echo timeout $1
