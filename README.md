# 北京邮电大学计算机学院程序设计实践大作业 - 基于领域特定脚本语言的客服机器人的设计与实现（DSL）

## 本作业得到95分，如果能帮助到您的话，请给我点个Star⭐吧！😄

# CustomerServiceBots 项目文档

## 项目名称
基于领域特定脚本语言的客服机器人的设计与实现

## 概述
该项目通过**Python**实现了一个从语法树解析到运行的交互式解释器，支持用户在Web端完成注册、登录、交互等操作，并基于Flask提供RESTful API服务。项目采用模块化设计，包括词法分析、语法分析和解释器执行，并支持简单的流程定义和动态变量管理。

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

## 运行方法

### 1. 安装依赖

确保已经安装了以下依赖：

```
cd frontEnd
npm install
cd..

cd backEnd
pip install -r requirements.txt
cd..
```

### 2. 启动后端服务

在`backEnd`目录下运行以下命令启动后端服务：

```
cd backEnd
python app.py
```

### 3. 启动前端服务

在`frontEnd`目录下运行以下命令启动前端服务：

```
cd frontEnd
npm run dev
```

### 4. 访问应用

打开浏览器，访问`http://localhost:5173`即可使用应用。

## 代码风格

### 1. 代码注释

- **详细性**: 代码中普遍存在详细的注释，尤其是在类和方法定义部分。注释清晰地解释了每个方法的功能、参数和返回值。例如，在`Root`类中，方法如`addStep`和`addVarName`都有明确的注释说明其用途和参数要求。这种详细性确保了开发人员能够快速理解每个方法的目的和使用方法。
- **一致性**: 注释风格在整个项目中保持一致，通常在方法定义的上方提供简要说明。这种一致性有助于提高代码的可读性和维护性，特别是在多人协作的环境中，确保团队成员之间的沟通顺畅。

### 2. 命名

- **直观性**: 变量、方法和类的命名大多是直观和有意义的，使得代码易于理解。例如，`getStep`、`setMainStep`、`processTokens`等方法名称直接反映了其功能。这样的命名方式使得代码本身就像文档一样，减少了对外部文档的依赖。
- **风格统一**: 命名风格在项目中保持一致，使用驼峰命名法（CamelCase）来命名方法和类，符合Python的命名惯例。这种一致性使得代码在视觉上更加整齐，并且符合Python开发者的期望。

### 3. 代码格式

- **格式整齐**: 代码格式整齐，缩进和空行使用得当，便于阅读。每个模块的代码结构都遵循良好的编程习惯，确保了代码的可读性。良好的格式使得代码块之间的关系更加清晰，便于理解程序的流程。
- **模块化**: 代码被分成多个模块，每个模块负责特定的功能，便于管理和理解。这种模块化设计不仅提高了代码的可维护性，还允许开发人员在不影响整体系统的情况下修改或替换某个模块。

### 数据结构

- **Root类**: 负责管理整个语法树，包括步骤表（`stepTable`）、主要步骤（`mainStep`）、变量名列表（`varName`）和分支表（`branchTable`）。通过方法如`addStep`、`addVarName`、`addBranch`等来操作这些数据结构。这种设计使得语法树的管理变得高效和有条理。
- **Step类**: 用于表示一个步骤，包括步骤ID（`stepID`）和步骤内容（`step`）。提供方法如`setStepID`和`addStep`来管理步骤信息。该类的设计使得步骤的定义和操作独立于其他逻辑，增强了代码的复用性。
- **Expression类**: 用于存储和管理表达式，提供方法如`addExpr`和`getExpr`来操作表达式数据。表达式的抽象管理使得复杂的表达式处理变得简单和模块化。
- **UserTable类**: 用于管理用户信息，存储在字典`userTable`中，提供方法如`setName`和`setUser`来管理用户数据。用户信息的集中管理使得数据访问和修改变得高效。

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

## 接口

### 1. 程序间接口

### 程序间接口

#### 模块间接口

##### 1. DataStructure与其他模块

- **接口功能**: `DataStructure.py`中的类提供了基础数据结构，用于存储和管理脚本执行过程中需要的数据。
- **接口方法**:
  - `Root`类提供方法如`addStep`、`addVarName`，供其他模块调用以构建和修改语法树。
  - 其他模块通过实例化这些类，调用其方法来操作和查询数据。

##### 2. Lexical与Grammar

- **接口功能**: `Lexical.py`负责将输入的文本文件解析为词法单元，然后将这些词法单元提供给`Grammar.py`进行语法分析。
- **接口方法**:
  - `Lexical`类提供方法`tokenize`，返回解析后的词法单元列表。
  - `Grammar`模块调用`Lexical`的`tokenize`方法，获取词法单元列表，作为语法解析的输入。

##### 3. Grammar与Interpreter

- **接口功能**: `Grammar.py`负责将词法单元解析为语法树，然后将该语法树传递给`Interpreter.py`来执行。
- **接口方法**:
  - `Grammar`类提供方法`parse`，返回构建的语法树。
  - `Interpreter`模块通过调用`Grammar`的`parse`方法，获取语法树，并通过其接口方法来执行解析后的脚本。

##### 4. Interpreter与app

- **接口功能**: `Interpreter.py`负责根据语法树执行脚本，并将执行结果传递给`app.py`，从而通过API接口返回给用户。
- **接口方法**:
  - `Interpreter`类提供方法如`executeStep`，用于执行特定的步骤。
  - `app.py`通过实例化`Interpreter`，调用其方法来执行用户请求的脚本，并获取结果以返回给客户端。

#### 数据流与控制流

- **数据流**: 数据在模块间通过方法返回值和参数传递。例如，词法单元列表从`Lexical`传递到`Grammar`，语法树从`Grammar`传递到`Interpreter`。
- **控制流**: 控制流通过方法调用来实现。每个模块负责特定的处理阶段，调用下一个模块的方法来传递控制权。

####  接口设计原则

- **低耦合**: 各模块之间通过明确的接口进行交互，减少了模块之间的依赖，便于独立开发和测试。
- **高内聚**: 每个模块内部实现其核心功能，模块之间通过接口进行交互，保证了模块的职责单一和内聚性。
- **接口清晰**: 接口方法的名称和参数设计直观且具有描述性，便于理解和使用。

### 人机接口

#### 1. Flask应用结构

- **Flask框架**: 项目使用Flask来构建Web应用，提供HTTP接口供客户端调用。
- **应用初始化**: 在`app.py`中初始化Flask应用，并定义不同的路由和处理函数。

#### 2. API端点

##### 2.1 用户注册接口

- **端点**: `/register`
- **方法**: `POST`
- **描述**: 处理用户注册请求，接收用户信息并存储在系统中。
- **请求参数**:
  - `username`: 用户名
  - `password`: 密码
- **响应**:
  - 成功注册时返回状态码200和成功消息。
  - 如果用户已存在则返回状态码400和错误消息。

##### 2.2 用户登录接口

- **端点**: `/login`
- **方法**: `POST`
- **描述**: 处理用户登录请求，验证用户凭据。
- **请求参数**:
  - `username`: 用户名
  - `password`: 密码
- **响应**:
  - 成功登录时返回状态码200和成功消息。
  - 如果凭据无效则返回状态码401和错误消息。

##### 2.3 信息获取与设置接口

- **端点**: `/user/info`
- **方法**: `GET` / `POST`
- **描述**: 获取或更新用户的信息。
- **请求参数**:
  - `GET`请求无需参数，返回当前用户信息。
  - `POST`请求需要用户信息参数，用于更新用户信息。
- **响应**:
  - 成功获取或更新时返回状态码200和相关信息。
  
##### 2.4 清除对话接口

- **端点**: `/clear`
- **方法**: `POST`
- **描述**: 清除当前用户的对话记录。
- **请求参数**: 无需参数。
- **响应**:
  - 成功清除时返回状态码200和成功消息。

##### 2.5 用户输入处理接口

- **端点**: `/execute`
- **方法**: `POST`
- **描述**: 处理用户输入的脚本，解释并执行。
- **请求参数**:
  - `script`: 用户输入的脚本内容。
- **响应**:
  - 返回执行结果，包括状态码200和执行输出。
  - 如果脚本有误则返回状态码400和错误消息。

#### 3. 请求与响应格式

- **请求格式**: 所有请求参数通过JSON格式传递，确保数据结构化和易于解析。
- **响应格式**: 响应数据也使用JSON格式，包含状态码、消息和必要的返回数据。

#### 4. 安全性

- **身份验证**: 用户登录后，系统可以通过会话或令牌机制保持用户状态，确保只有经过身份验证的用户可以访问受保护的资源。
- **数据验证**: 所有输入数据在服务器端进行验证，防止恶意输入导致的安全问题。

#### 5. 用户体验

- **实时性**: API设计支持快速响应用户请求，提供实时的操作反馈。
- **易用性**: 通过RESTful设计，接口语义清晰，便于客户端开发人员理解和使用。

## 自动测试脚本

```
test_script.py
```

### 概述

本次测试的目的是验证Web应用程序中的注册、登录、信息设置、以及客服功能的正确性。测试脚本使用Selenium自动化工具进行编写，主要测试以下功能模块：

1. 用户注册
2. 用户登录
3. 信息设置
4. 客服功能

### 测试环境

- 浏览器：Microsoft Edge
- Selenium WebDriver
- 操作系统：假设为Windows
- 测试地址：http://localhost:5173/

### 测试步骤

1. **用户注册**
   - 打开首页
   - 点击注册按钮
   - 填写用户名和密码
   - 提交注册表单
   - 验证注册成功提示

2. **用户登录**
   - 打开首页
   - 点击登录按钮
   - 填写用户名和密码
   - 提交登录表单
   - 验证登录成功提示

3. **信息设置**
   - 登录后点击信息设置按钮
   - 填写个人信息表单（姓名和金额）
   - 提交信息表单
   - 验证信息提交成功提示

4. **客服功能**
   - 登录后点击客服按钮
   - 验证客服的初始输出
   - 输入投诉文本并提交
   - 验证客服的响应
   - 输入账单文本并提交
   - 验证客服的响应

### 测试结果

- **用户注册**：成功
  - 注册按钮点击正常，注册表单提交成功，成功提示显示正确。
  
- **用户登录**：成功
  - 登录按钮点击正常，登录表单提交成功，成功提示显示正确。

- **信息设置**：成功
  - 信息设置按钮点击正常，信息表单提交成功，成功提示显示正确。

- **客服功能**：成功
  - 客服按钮点击正常，初始客服输出正确。
  - 投诉文本提交后，客服响应正确。
  - 账单文本提交后，客服响应正确。

### 截图

测试过程中进行了多个步骤的截图以便于验证和调试。所有截图均已保存至`screenshots`目录。具体截图包括：

- 页面加载后的截图
- 每个主要步骤（如点击按钮、提交表单）后的截图
- 成功和失败提示的截图

### 日志

日志文件`selenium_test.log`记录了测试过程中所有的操作、成功和失败的详细信息。日志级别设定为INFO，涵盖了测试的每一个步骤。

```
2024-12-27 16:32:32,041 - INFO - 已启动Edge浏览器实例
2024-12-27 16:32:32,041 - INFO - 打开首页: http://localhost:5173/
2024-12-27 16:32:32,712 - INFO - 截图已保存到: screenshots\homepage_loaded_20241227_163232.png
2024-12-27 16:32:32,720 - INFO - 页面容器已加载
2024-12-27 16:32:32,721 - INFO - 尝试点击注册按钮
2024-12-27 16:32:32,741 - INFO - 找到注册按钮，尝试点击
2024-12-27 16:32:33,005 - INFO - 使用Actions类成功点击元素
2024-12-27 16:32:33,006 - INFO - 已点击注册按钮
2024-12-27 16:32:33,161 - INFO - 截图已保存到: screenshots\after_click_register_20241227_163233.png
2024-12-27 16:32:33,161 - INFO - 填写注册表单
2024-12-27 16:32:33,282 - INFO - 已填写用户名和密码
2024-12-27 16:32:33,283 - INFO - 提交注册表单
2024-12-27 16:32:33,350 - INFO - 已点击提交注册表单按钮
2024-12-27 16:32:33,350 - INFO - 验证注册是否成功
2024-12-27 16:32:33,936 - INFO - 注册成功
2024-12-27 16:32:34,028 - INFO - 截图已保存到: screenshots\registration_success_20241227_163233.png
2024-12-27 16:32:37,029 - INFO - 填写登录表单
2024-12-27 16:32:37,122 - INFO - 已填写登录用户名和密码
2024-12-27 16:32:37,122 - INFO - 提交登录表单
2024-12-27 16:32:37,173 - INFO - 已点击提交登录表单按钮
2024-12-27 16:32:37,173 - INFO - 验证登录是否成功
2024-12-27 16:32:37,712 - INFO - 登录成功
2024-12-27 16:32:37,799 - INFO - 截图已保存到: screenshots\login_success_20241227_163237.png
2024-12-27 16:32:40,799 - INFO - 尝试点击客服按钮
2024-12-27 16:32:40,820 - INFO - 找到客服按钮，尝试点击
2024-12-27 16:32:41,111 - INFO - 使用Actions类成功点击元素
2024-12-27 16:32:41,111 - INFO - 已点击客服按钮
2024-12-27 16:32:41,233 - INFO - 截图已保存到: screenshots\after_click_customer_20241227_163241.png
2024-12-27 16:32:44,234 - INFO - 检查客服输出1
2024-12-27 16:32:44,258 - INFO - 客服输出正确
2024-12-27 16:32:44,352 - INFO - 截图已保存到: screenshots\customer_service_correct_20241227_163244.png
2024-12-27 16:32:54,353 - INFO - 检查客服输出2
2024-12-27 16:32:54,380 - INFO - 客服输出正确
2024-12-27 16:32:54,480 - INFO - 截图已保存到: screenshots\customer_service_correct_20241227_163254.png
2024-12-27 16:32:57,481 - INFO - 输入文本
2024-12-27 16:32:57,530 - INFO - 已填写文本投诉
2024-12-27 16:32:57,530 - INFO - 提交文本投诉
2024-12-27 16:32:57,612 - INFO - 已点击提交文本投诉按钮
2024-12-27 16:32:57,613 - INFO - 验证是否提交文本投诉成功
2024-12-27 16:32:57,640 - INFO - 提交文本投诉成功
2024-12-27 16:32:57,750 - INFO - 截图已保存到: screenshots\submit_text_success_20241227_163257.png
2024-12-27 16:33:00,751 - INFO - 检查客服输出3
2024-12-27 16:33:00,780 - INFO - 客服输出正确
2024-12-27 16:33:00,885 - INFO - 截图已保存到: screenshots\customer_service_correct_20241227_163300.png
2024-12-27 16:33:03,885 - INFO - 输入文本
2024-12-27 16:33:03,932 - INFO - 已填写文本账单
2024-12-27 16:33:03,933 - INFO - 提交文本账单
2024-12-27 16:33:04,004 - INFO - 已点击提交文本账单按钮
2024-12-27 16:33:04,004 - INFO - 验证是否提交文本账单成功
2024-12-27 16:33:04,031 - INFO - 提交文本账单成功
2024-12-27 16:33:04,167 - INFO - 截图已保存到: screenshots\submit_text_success_20241227_163304.png
2024-12-27 16:33:07,168 - INFO - 检查客服输出4
2024-12-27 16:33:07,194 - INFO - 客服输出正确
2024-12-27 16:33:07,286 - INFO - 截图已保存到: screenshots\customer_service_correct_20241227_163307.png
2024-12-27 16:33:07,287 - INFO - 客服测试1 正确
2024-12-27 16:33:07,383 - INFO - 截图已保存到: screenshots\all_correct_20241227_163307.png
2024-12-27 16:33:07,384 - INFO - 关闭浏览器
2024-12-27 16:33:11,207 - INFO - 已启动Edge浏览器实例
2024-12-27 16:33:11,207 - INFO - 打开首页: http://localhost:5173/
2024-12-27 16:33:11,896 - INFO - 截图已保存到: screenshots\homepage_loaded_20241227_163311.png
2024-12-27 16:33:11,905 - INFO - 页面容器已加载
2024-12-27 16:33:11,906 - INFO - 尝试点击登录按钮
2024-12-27 16:33:12,191 - INFO - 使用Actions类成功点击元素
2024-12-27 16:33:12,192 - INFO - 已点击登录按钮
2024-12-27 16:33:12,318 - INFO - 截图已保存到: screenshots\after_click_login_20241227_163312.png
2024-12-27 16:33:12,318 - INFO - 填写登录表单
2024-12-27 16:33:12,431 - INFO - 已填写登录用户名和密码
2024-12-27 16:33:12,431 - INFO - 提交登录表单
2024-12-27 16:33:12,492 - INFO - 已点击提交登录表单按钮
2024-12-27 16:33:12,493 - INFO - 验证登录是否成功
2024-12-27 16:33:13,046 - INFO - 登录成功
2024-12-27 16:33:13,129 - INFO - 截图已保存到: screenshots\login_success_20241227_163313.png
2024-12-27 16:33:16,130 - INFO - 尝试点击信息设置按钮
2024-12-27 16:33:16,151 - INFO - 找到信息设置按钮，尝试点击
2024-12-27 16:33:16,464 - INFO - 使用Actions类成功点击元素
2024-12-27 16:33:16,465 - INFO - 已点击信息设置按钮
2024-12-27 16:33:16,614 - INFO - 截图已保存到: screenshots\after_click_info_20241227_163316.png
2024-12-27 16:33:16,614 - INFO - 填写信息表单
2024-12-27 16:33:16,707 - INFO - 已填写信息表单
2024-12-27 16:33:16,707 - INFO - 提交信息表单
2024-12-27 16:33:16,772 - INFO - 已点击提交信息表单按钮
2024-12-27 16:33:16,772 - INFO - 验证是否提交信息表单成功
2024-12-27 16:33:17,310 - INFO - 提交信息表单成功
2024-12-27 16:33:17,419 - INFO - 截图已保存到: screenshots\info_commit_success_20241227_163317.png
2024-12-27 16:33:20,419 - INFO - 尝试点击客服按钮
2024-12-27 16:33:20,440 - INFO - 找到客服按钮，尝试点击
2024-12-27 16:33:20,728 - INFO - 使用Actions类成功点击元素
2024-12-27 16:33:20,729 - INFO - 已点击客服按钮
2024-12-27 16:33:20,837 - INFO - 截图已保存到: screenshots\after_click_customer_20241227_163320.png
2024-12-27 16:33:23,837 - INFO - 检查客服输出1
2024-12-27 16:33:23,867 - INFO - 客服输出正确
2024-12-27 16:33:23,969 - INFO - 截图已保存到: screenshots\customer_service_correct_20241227_163323.png
2024-12-27 16:33:26,970 - INFO - 输入文本
2024-12-27 16:33:27,019 - INFO - 已填写文本账单
2024-12-27 16:33:27,019 - INFO - 提交文本账单
2024-12-27 16:33:27,105 - INFO - 已点击提交文本账单按钮
2024-12-27 16:33:27,105 - INFO - 验证是否提交文本账单成功
2024-12-27 16:33:27,132 - INFO - 提交文本账单成功
2024-12-27 16:33:27,252 - INFO - 截图已保存到: screenshots\submit_text_success_20241227_163327.png
2024-12-27 16:33:30,252 - INFO - 检查客服输出2
2024-12-27 16:33:30,277 - INFO - 客服输出正确
2024-12-27 16:33:30,365 - INFO - 截图已保存到: screenshots\customer_service_correct_20241227_163330.png
2024-12-27 16:33:30,365 - INFO - 客服测试2 正确
2024-12-27 16:33:30,466 - INFO - 截图已保存到: screenshots\all_correct_20241227_163330.png
2024-12-27 16:33:30,466 - INFO - 客服测试全部正确
2024-12-27 16:33:30,567 - INFO - 截图已保存到: screenshots\all_correct_20241227_163330.png
2024-12-27 16:33:30,567 - INFO - 关闭浏览器
```

### 结论

本次测试脚本运行结果显示，所有功能模块均通过测试，达到了预期的功能要求。未发现任何功能性缺陷或错误。

### 建议

- 在实际项目中，建议将测试脚本集成到持续集成/持续交付（CI/CD）管道中，以便在每次代码变更后自动运行测试。
- 考虑扩展测试用例，涵盖更多异常情况和边界条件。
- 测试脚本中的静态等待时间（`time.sleep`）可以替换为更智能的等待条件，以提高测试效率和稳定性。

## 测试桩

### 概述

本报告涵盖了为多个模块编写的单元测试桩，包括Lexical、Grammar、DataStructure、Interpreter和App模块。这些测试桩旨在验证各个模块的基本功能，确保它们在预期的输入下能够正常工作。

### 测试环境

- 编程语言：Python
- 测试框架：unittest
- 目标模块：Lexical、Grammar、DataStructure、Interpreter、App

### 测试模块

#### 1. Lexical 模块

**目标：** 验证Lexical类的词法分析功能。

- **测试用例：**
  - `testLexicalParsing`: 测试词法解析功能是否能够正确解析输入文件并生成预期的词法单元。
  - `testPrintTokens`: 测试打印词法单元功能，确保输出格式和内容正确。

- **结果：** 所有测试用例通过，词法解析和打印功能正常。

#### 2. Grammar 模块

**目标：** 验证Grammar类的语法树构建、变量名处理及错误处理功能。

- **测试用例：**
  - `testGrammarTree`: 测试语法树构建，验证主步骤和步骤内容是否正确。
  - `testVariableNames`: 测试变量名处理，确保变量名能被正确解析和存储。
  - `testProcessError`: 测试错误处理机制，确保无效token会产生适当的错误信息。

- **结果：** 所有测试用例通过，语法树构建、变量名处理和错误处理功能正常。

#### 3. DataStructure 模块

**目标：** 验证数据结构模块中的Root、Step、Expression和UserTable类的基本功能。

- **测试用例：**
  - `TestRoot`: 测试Root类的初始化、步骤管理、变量名和分支管理功能。
  - `TestStep`: 测试Step类的初始化和步骤管理功能。
  - `TestExpression`: 测试Expression类的初始化和表达式管理功能。
  - `TestUserTable`: 测试UserTable类的初始化、用户信息设置和获取功能。

- **结果：** 所有测试用例通过，数据结构模块的各个类功能正常。

#### 4. Interpreter 模块

**目标：** 验证Interpreter类的Speak、Listen和Silence功能。

- **测试用例：**
  - `testInterpreterSpeak`: 测试Speak功能，验证输出的正确性。
  - `testInterpreterListenAndBranch`: 测试Listen和Branch功能，验证输入处理和分支选择的正确性。
  - `testInterpreterSilence`: 测试Silence功能，验证在无输入时的正确输出。

- **结果：** 所有测试用例通过，解释器的各项功能正常。

#### 5. App 模块

**目标：** 验证应用程序中API接口的功能，包括用户注册、登录、信息设置和聊天流程。

- **测试用例：**
  - `testRegisterAndLogin`: 测试用户注册和登录功能，验证成功和失败的处理。
  - `testGetAndSetInfo`: 测试用户信息的设置和获取功能。
  - `testChatFlow`: 测试完整的聊天流程，包括聊天记录的清除、获取和机器人回复。

- **结果：** 所有测试用例通过，API接口功能正常。

### 测试桩日志
```
(bots) D:\CustomerServiceBots\backEnd>sh script/testAll.sh
...............
----------------------------------------------------------------------
Ran 15 tests in 0.001s

OK
..
----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
...
----------------------------------------------------------------------
Ran 3 tests in 5.703s

OK
超时
No response received
['Step', 'welcome']
['Speak', '$name', '+', '"您好，请问有什么可以帮您?"']
['Listen', '10']
['Branch', '"投诉"', 'complainProc']
['Branch', '"账单"', 'billProc']
['Silence', 'silenceProc']
['Default', 'defaultProc']
['Step', 'complainProc']
['Speak', '"您的意见是我们改进工作的动力，请问您还有什么补充?"']
['Listen', '10']
['Default', 'thanks']
['Step', 'thanks']
['Speak', '"感谢您的来电，再见"']
['Exit']
['Step', 'billProc']
['Speak', '"您的本月账单是"', '+', '$amount', '+', '"元，感谢您的来电，再见"']
['Exit']
['Step', 'silenceProc']
['Speak', '"听不清，请您大声一点可以吗"']
['Listen', '10']
['Branch', '"投诉"', 'complainProc']
['Branch', '"账单"', 'billProc']
['Silence', 'silenceProc']
['Default', 'defaultProc']
['Step', 'defaultProc']
['Exit']
{'welcome': [['Speak', 'name', '您好，请问有什么可以帮您?'], ['Listen', '10'], ['Branch'], ['Silence', 'silenceProc'], ['Default', 'defaultProc']], 'complainProc': [['Speak', '您的意见是我们改进工作的动力，请问您还有什么补充?'], ['Listen', '10'], ['Default', 'thanks']], 'thanks': [['Speak', '感谢 您的来电，再见'], ['Exit']], 'billProc': [['Speak', '您的本月账单是', 'amount', '元，感谢您的来电，再见'], ['Exit']], 'silenceProc': [['Speak', '听不清，请您大声一点可以吗'], ['Listen', '10'], ['Branch'], ['Silence', 'silenceProc'], ['Default', 'defaultProc']], 'defaultProc': [['Exit']]}
['name', 'amount']
{'投诉': 'complainProc', '账单': 'billProc'}
testuser
testuser您好，请问有什么可以帮您?
.name Alice
amount 100
..
----------------------------------------------------------------------
Ran 3 tests in 0.018s

OK
```

### 结论

通过本次测试桩的执行，各模块的基本功能均通过验证，表现出预期的行为。测试桩覆盖了主要功能点，确保了模块在正常输入下的可靠性。为了进一步提高测试覆盖率，建议在未来的测试中增加更多的边界条件和异常输入测试。