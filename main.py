import PySimpleGUI as sg
import requests

# --- 核心功能函数 ---
def get_gists(token):
    """
    根据Token获取用户的Gist列表
    """
    url = "https://api.github.com/gists"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        # 发送GET请求
        response = requests.get(url, headers=headers, timeout=10)
        
        # 如果状态码是200，说明成功
        if response.status_code == 200:
            return response.json()
        else:
            # 返回错误信息
            return {"error": f"Error: {response.status_code}", "message": response.text}
            
    except Exception as e:
        return {"error": "Exception", "message": str(e)}

# --- 界面布局 ---
sg.theme('SystemDefault') # 使用系统默认主题

layout = [
    [sg.Text("请输入你的 GitHub Token:", font=("Microsoft YaHei", 12))],
    [sg.InputText(key='-TOKEN-', password_char='*', font=("Microsoft YaHei", 12))],
    [sg.Button('获取 Gist 列表', font=("Microsoft YaHei", 12), key='-FETCH-'), sg.Button('退出', font=("Microsoft YaHei", 12))],
    [sg.HorizontalSeparator()],
    [sg.Text("结果输出:", font=("Microsoft YaHei", 12))],
    [sg.Listbox(values=[], size=(50, 10), key='-OUTPUT-', font=("Microsoft YaHei", 10))]
]

# --- 创建窗口 ---
window = sg.Window('GitHub Gist 查看器', layout, finalize=True)

# --- 事件循环 ---
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, '退出'):
        break
        
    if event == '-FETCH-':
        token = values['-TOKEN-'].strip()
        
        if not token:
            sg.popup_error("Token 不能为空！")
            continue
            
        # 更新界面提示正在加载
        window['-OUTPUT-'].update(['正在从 GitHub 获取数据，请稍候...'])
        window.refresh()
        
        # 调用核心功能
        data = get_gists(token)
        
        # 处理返回结果
        display_list = []
        if isinstance(data, list):
            for gist in data:
                # 简单提取文件名和更新时间
                files = ", ".join(gist['files'].keys())
                updated_at = gist['updated_at']
                display_list.append(f"[{updated_at[:10]}] {files}")
        else:
            # 出错了
            display_list = [f"获取失败: {data.get('error')}", f"详情: {data.get('message')}"]
            
        # 更新列表显示
        window['-OUTPUT-'].update(display_list)

window.close()