安装uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

安装依赖和虚拟环境
cd ai-test-agent-system
uv sync

修改.env 中的key
cat .env
DEEPSEEK_API_KEY
