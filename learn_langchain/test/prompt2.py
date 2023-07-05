import os
from langchain.prompts.example_selector.base import BaseExampleSelector
from typing import Dict, List
import numpy as np
from dotenv import load_dotenv
load_dotenv()

# Example Selectorの使い方
class CustomExampleSelector(BaseExampleSelector):

    def __init__(self, examples: List[Dict[str, str]]):
        self.examples = examples

    def add_example(self, example: Dict[str, str]) -> None:
        """新しい教師データを格納するための関数"""
        self.examples.append(example)

    def select_examples(self, input_variables: Dict[str, str]) -> List[dict]:
        """教師データを選択するための関数"""
        return np.random.choice(self.examples, size=2, replace=False)
    
examples = [
    {"fruit": "りんご", "color": "赤"},
    {"fruit": "キウイ", "color": "緑"},
    {"fruit": "ぶどう", "color": "紫"},
]

# 教師データの登録
example_selector = CustomExampleSelector(examples)

# 教師データの出力
print("教師データの出力:",example_selector.examples)

# 教師データの追加
example_selector.add_example({"fruit": "オレンジ", "color": "橙"} )
print("教師データの追加:",example_selector.examples, "\n")

# 教師データの選択
print("教師データの選択:",example_selector.select_examples({"fruit": "fruit"}))