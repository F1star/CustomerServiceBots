# CustomerServiceBots 项目文档

## 项目名称
基于领域特定脚本语言的客服机器人的设计与实现

---

## 概述
该项目通过**Python**实现了一个从语法树解析到运行的交互式解释器，支持用户在Web端完成注册、登录、交互等操作，并基于Flask提供RESTful API服务。项目采用模块化设计，包括词法分析、语法分析和解释器执行，并支持简单的流程定义和动态变量管理。

---

## 记法描述
该脚本语言具有以下语法规则：
1. **命令格式**：每条语句以关键字开头，后接参数。
   - 关键字包括：`Step`、`Speak`、`Listen`、`Branch`、`Silence`、`Default`、`Exit`。
2. **语法一般规则**：
   - **`Step`**：定义步骤的开始，后接步骤ID。
     ```plaintext
     Step StepID
     ```
   - **`Speak`**：输出字符串或变量，支持多个拼接。
     ```plaintext
     Speak "Hello" + $variable + "World"
     ```
   - **`Listen`**：监听用户输入，后接超时时间（秒）。
     ```plaintext
     Listen 5
     ```
   - **`Branch`**：条件分支，格式为`Branch 条件 下一步`。
     ```plaintext
     Branch "yes" NextStep
     ```
   - **`Silence`**：静默等待，后接超时时间（秒）。
     ```plaintext
     Silence SilenceStep
     ```
   - **`Default`**：默认分支，后接下一步。
     ```plaintext
     Default DefaultStep
     ```
   - **`Exit`**：结束当前流程。
     ```plaintext
     Exit
     ```
3. **语法特殊规则**：
   - 变量表示必须以`$`开头。
   - 字符串必须用双引号括起来。
   - 每个 `Step` 看作一个流程，每个流程有三种形式 (括号是可有可无的) ：
      - `Step -- Speak -- Listen -- Branch -- Silence -- Default`
      - `Step -- Speak -- (Listen) -- Default`
      - `Step -- (Speak) -- Exit`
   - 通篇代码中必须要有一个 `Exit` 语句。
   - 一个流程中不能出现有两个相邻的 `Speak` 语句。
   - 一个流程中可以出现 0 个或多个 `Branch` 语句。
   - 若一个流程是 `Step -- Speak -- (Listen) -- Default` 结构，则 Default 流程必须是 `Step -- Exit` 结构。
---

## 功能模块
### 1. 数据结构模块（`DataStructure.py`）
该模块定义了解释器所需的核心数据结构：
- **`Root`**：语法树的根节点，管理步骤、变量、分支等。
- **`Step`**：定义具体的步骤及操作。
- **`Expression`**：表达式对象，用于存储语法分析中的表达式。
- **`UserTable`**：管理用户信息（变量名和具体值）。

#### 数据结构示例
```python
# 创建语法树根节点
root = Root()
root.addStep("Step1", ["Speak", "Hello"])
root.setMainStep("Step1")
root.addVarName("username")
```

### 2. 词法分析模块（`Lexical.py`）
实现对输入脚本文件的词法分析，将代码分割为可供语法分析的**Token**序列。

**功能要点**：
- **忽略空行和注释**：支持以`#`开头的注释行。
- **生成Token流**：通过`getTokens`获取分析结果。

#### 示例
输入文件内容：
```
Step Start
Speak "Hello, world"
Listen 5
Branch "yes" Step2
Exit
```

生成的Token：
```python
[['Step', 'Start'], ['Speak', '"Hello,', 'world"'], ['Listen', '5'], ['Branch', '"yes"', 'Step2'], ['Exit']]
```

### 3. 语法分析模块（`Grammar.py`）
基于Token流生成语法树的核心模块，支持以下命令：
- **`Step`**：定义步骤。
- **`Speak`**：输出语句。
- **`Listen`**：监听用户输入。
- **`Branch`**：分支控制。
- **`Silence`**/**`Default`**/**`Exit`**：流程控制。

#### 功能要点
- 自动构建并管理语法树。
- 检查变量使用的合法性，动态记录变量名。
- 报错提示：检测非法语法并输出错误信息。

#### 示例
Token流：
```python
[['Step', 'Start'], ['Speak', '"Hello"'], ['Listen', '5'], ['Branch', '"yes"', 'Step2'], ['Exit']]
```

生成语法树：
```python
{
    "mainStep": "Start",
    "stepTable": {
        "Start": [
            ['Speak', 'Hello'],
            ['Listen', '5'],
            ['Branch', 'yes', 'Step2'],
            ['Exit']
        ]
    },
    "branchTable": {
        "yes": "Step2"
    }
}
```

### 4. 解释器模块（`Interpreter.py`）
核心模块，负责执行基于语法树的指令，支持多用户并发操作。实现以下功能：
- **步骤调度**：按顺序解析语法树的每一步。
- **动态变量处理**：基于用户输入完成变量的替换和存储。
- **多线程支持**：通过线程控制用户输入的超时与结果锁。

#### 功能要点
- **`dispatch`**：执行流程的主方法。
- **`doSpeak`**：处理输出表达式。
- **`doListen`**：监听用户输入并判断超时。
- **多用户环境**：通过`UserTable`存储每个用户的上下文。

---

## Web服务模块（`app.py`）
通过**Flask**提供Web接口，支持用户管理与解释器调用。

### 提供的API
| API           | 方法  | 功能描述              |
|---------------|-------|-----------------------|
| `/register`   | POST  | 用户注册             |
| `/login`      | POST  | 用户登录并初始化解释器 |
| `/getinfo`    | POST  | 获取用户变量名列表     |
| `/setinfo`    | POST  | 设置用户变量的值       |
| `/clearchat`  | POST  | 执行解释器的`dispatch`方法 |
| `/telechat`   | POST  | 提交用户输入           |
| `/repeatchat` | POST  | 获取解释器的最新输出   |

---

## 测试覆盖率
1. **单元测试**：对每个模块方法（如`addStep`, `processTokens`）编写单元测试。
2. **集成测试**：使用`pytest`测试API和解释器的交互。
3. **自动测试脚本**：
   - 模拟用户提交Token文件。
   - 测试超时行为和分支控制。