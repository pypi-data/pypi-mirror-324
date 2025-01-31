from quantalogic.model_info import ModelInfo

model_info = {
    "dashscope/qwen-max": ModelInfo(
        model_name="dashscope/qwen-max",
        max_output_tokens=8 * 1024,
        max_input_tokens=32 * 1024,
    ),
    "dashscope/qwen-plus": ModelInfo(
        model_name="dashscope/qwen-plus",
        max_output_tokens=8 * 1024,
        max_input_tokens=131072,
    ),
    "dashscope/qwen-turbo": ModelInfo(
        model_name="dashscope/qwen-turbo",
        max_output_tokens=8 * 1024,
        max_input_tokens=1000000,
    ),
    "deepseek-reasoner": ModelInfo(
        model_name="deepseek-reasoner",
        max_output_tokens=8 * 1024,
        max_input_tokens=1024 * 128,
    ),
    "openrouter/deepseek/deepseek-r1": ModelInfo(
        model_name="openrouter/deepseek/deepseek-r1",
        max_output_tokens=8 * 1024,
        max_input_tokens=1024 * 128,
    ),
    "openrouter/mistralai/mistral-large-2411": ModelInfo(
        model_name="openrouter/mistralai/mistral-large-2411",
        max_output_tokens=128 * 1024,
        max_input_tokens=1024 * 128,
    ),
    "mistralai/mistral-large-2411": ModelInfo(
        model_name="mistralai/mistral-large-2411",
        max_output_tokens=128 * 1024,
        max_input_tokens=1024 * 128,
    ),
    "deepseek/deepseek-chat": ModelInfo(
        model_name="deepseek/deepseek-chat",
        max_output_tokens=8 * 1024,
        max_input_tokens=1024 * 64,
    ),
    "deepseek/deepseek-reasoner": ModelInfo(
        model_name="deepseek/deepseek-reasoner",
        max_output_tokens=8 * 1024,
        max_input_tokens=1024 * 64,
        max_cot_tokens=1024 * 32,
    ),
    "nvidia/deepseek-ai/deepseek-r1": ModelInfo(
        model_name="nvidia/deepseek-ai/deepseek-r1",
        max_output_tokens=8 * 1024,
        max_input_tokens=1024 * 64,
    ),
    

}
