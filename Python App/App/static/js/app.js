document.addEventListener('DOMContentLoaded', () => {
    // 删除确认
    const deleteForms = document.querySelectorAll('form[method="POST"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (confirm('确定要删除该帖子吗？此操作不可撤销。')) {
                form.submit();
            }
        });
    });
    // 标签搜索建议
    const tagInput = document.querySelector('input[name="tag"]');
    if (tagInput) {
        let tagsCache = [];

        // 获取已存在的标签（简化实现）
        const tagElements = document.querySelectorAll('.tag-cloud .tag');
        tagElements.forEach(tag => {
            tagsCache.push(tag.textContent.split(' ')[0]);
        });

        // 创建datalist
        const dataList = document.createElement('datalist');
        dataList.id = 'tag-suggestions';
        tagInput.parentElement.appendChild(dataList);

        // 添加options
        tagsCache.forEach(tag => {
            const option = document.createElement('option');
            option.value = tag;
            dataList.appendChild(option);
        });

        tagInput.setAttribute('list', 'tag-suggestions');
    }

    // 简单的文本编辑器增强
    const editors = document.querySelectorAll('textarea[name="content"]');
    editors.forEach(editor => {
        editor.addEventListener('input', function() {
            this.style.height = 'inherit';
            this.style.height = `${this.scrollHeight}px`;
        });
    });
});