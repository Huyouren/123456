// 功能一：切换夜间模式
// 1. 获取需要操作的元素
const darkModeButton = document.getElementById('toggle-dark-mode');
const bodyElement = document.body;
// 2. 监听按钮的点击事件
darkModeButton.addEventListener('click', function() {
    // 3. 执行切换操作：检查body是否有一个叫'dark-mode'的class
    //    如果有，就移除它；如果没有，就添加它。
    bodyElement.classList.toggle('dark-mode');
});

// 功能二：动态添加项目经历
// 1. 获取元素
const addProjectBtn = document.getElementById('add-project-btn');
const newProjectInput = document.getElementById('new-project-input');
const projectList = document.querySelector('.section-title + .list-group'); // 获取紧跟在.section-title后的.list-group
// 2. 监听按钮点击
addProjectBtn.addEventListener('click', function() {
    // 3. 获取输入框的值
    const newProjectText = newProjectInput.value;

    // 4. 检查输入是否为空
    if (newProjectText.trim() === '') {
        alert('请输入项目名称！');
        return; // 结束函数执行
    }

    // 5. 创建一个新的列表项 <li>
    const newListItem = document.createElement('li');
    newListItem.className = 'list-group-item'; // 添加Bootstrap的class
    newListItem.textContent = newProjectText; // 设置文本内容

    // 6. 将新的列表项添加到列表中
    projectList.appendChild(newListItem);

    // 7. 清空输入框
    newProjectInput.value = '';
});

// --- jQuery 功能 ---
// 等待整个文档加载完成后再执行jQuery代码，这是标准做法
$(document).ready(function() {
    // 功能三：点击技能项后隐藏
    // 1. 选择 #skills-list 里的所有 li 元素
    // 2. 使用 .on() 方法绑定 click 事件
    $('#skills-list li').on('click', function() {
        // 'this' 在这里指的是被点击的那个li元素
        // 使用 .fadeOut() 方法实现淡出效果
        $(this).fadeOut();
    });
    // 1. 选择紧跟在“个人简介”标题后的 #bio-content 的父级h2
    const bioTitle = $('#bio-content').prev('.section-title');
    // 2. 修改鼠标样式，提示用户这里可以点击
    bioTitle.css('cursor', 'pointer');
    // 3. 绑定点击事件
    bioTitle.on('click', function() {
    // 使用 .slideToggle() 方法实现平滑的滑动展开/收起效果
    $('#bio-content').slideToggle();
    });
});