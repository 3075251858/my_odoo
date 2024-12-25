
let services = document.getElementById('services');
let combo = document.getElementById('combo');
let month_of_purchase = document.getElementById('month_of_purchase');
let price = document.getElementById('price');
let total_price = document.getElementById('total_price');
let note = document.getElementById('note');
let whitespace = document.getElementById('whitespace');
services.onchange = function(){
    if(validation(month_of_purchase.value)){
        requirePrice()
    }
}
combo.onchange = function(){
    if(validation(month_of_purchase.value)){
        requirePrice()
    }
}
month_of_purchase.onchange = function(){
    if(validation(month_of_purchase.value)){
        requirePrice()
    }else{
    alert('购买月不能小于1')
    }
}

function validation(number){
    if(number < 1){
        return false
    }else{
        return true
    }
}

function requirePrice(services, combo, purchase_of_month){
    const Http = new XMLHttpRequest();
    const url='http://127.0.0.1:8069/mobile/price';
    Http.open("post", url);
    Http.setRequestHeader("Content-Type", "application/json"); // 设置请求头为 JSON
    let data = JSON.stringify({
            "params": {
            "services": this.services.value,
            "combo": this.combo.value,
            "month_of_purchase":this.month_of_purchase.value
        }
    });
    Http.send(data);
    Http.onreadystatechange = (e) => {
        let data = JSON.parse(Http.responseText)
        document.getElementById('price').innerText = data.result.price;
        document.getElementById('total_price').innerText = data.result.total_price;

    }
}

//保存整条数据
document.getElementById('confirm').onclick = function(){
    const Http = new XMLHttpRequest();
    const url = 'http://127.0.0.1:8069/mobile/save_quotation';
    Http.open("POST", url); // 使用 POST 方法
    Http.setRequestHeader("Content-Type", "application/json"); // 设置请求头为 JSON
    console.log(price)
    // 创建要发送的 JSON 数据
    const data = JSON.stringify({
            "params": {
            "services": services.value,
            "combo": combo.value,
            "month_of_purchase": month_of_purchase.value,
            "price": price.innerHTML,
            "total_price": total_price.innerHTML,
            "note": note.value,
            "whitespace": whitespace.value
        }
    });

    Http.onreadystatechange = (e) => {
        if (Http.readyState === 4 && Http.status === 200) {
//        获取返回的数据id
            let data = JSON.parse(Http.responseText)
//        请求pdf文件预览
            requirePDF(data.result.record_id)
         } else if (Http.readyState === 4) {
            console.error("Error fetching PDF:", Http.statusText);
        }
    }
    Http.send(data);
}

let currentPdfUrl = null;
function requirePDF(record_id){
    const Http = new XMLHttpRequest();
    const url='http://127.0.0.1:8069/mobile/responsePDF?id='+record_id;

     // 显示加载状态
    let previewArea = document.getElementById('pdf_context');
    previewArea.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">加载中...</span></div></div>';

    // 显示模态框
    let pdfModal = document.getElementById('myModal');
    openModal(pdfModal)
    Http.open("get", url);
    Http.responseType = 'arraybuffer'; // 确保接收的是二进制数据
    Http.send();
    Http.onreadystatechange = (e) => {
       if (Http.readyState === 4) { // 确保请求完成
        if (Http.status === 200) { // 确保请求成功
            // 创建一个Blob对象
            const blob = new Blob([Http.response], { type: 'application/pdf' });

            // 创建URL对象
            currentPdfUrl = window.URL.createObjectURL(blob);

            // 在模态框中显示PDF
            previewArea.innerHTML = `
                <iframe src="${currentPdfUrl}" width="100%" height="500px" frameborder="0"></iframe>
            `;

            // 不要立即释放URL对象，等到模态框关闭时再释放
             URL.revokeObjectURL(currentPdfUrl);

             // 处理确认按钮点击事件,确认后下载pdf
            const confirmButton = document.getElementById('confirmButton');
            confirmButton.onclick = function() {
                console.log('确认按钮被点击');
                // 下载 PDF 文件
                const blob = new Blob([Http.response], { type: 'application/pdf' });
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = 'report.pdf'; // 设置下载文件名
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(downloadUrl);
//                将pdf上传到服务器保存
                // 上传 PDF 文件
                const formData = new FormData();
                formData.append('file', blob, 'report.pdf');

                fetch('/mobile/upload_pdf', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Upload successful:', data);
                })
                .catch(error => {
                    console.error('Error uploading PDF:', error);
                    alert('Failed to upload PDF. Please try again.');
                });

             // 关闭模态框
             let pdfModal = document.getElementById('myModal');
             pdfModal.style.display = 'none';
            }
        } else {
            console.error('Failed to load PDF:', Http.statusText);
            alert('Failed to load PDF. Please try again.');
        }
    }
    }
}
//关闭模态框
document.getElementById('close').onclick = function(){
    let pdfModal = document.getElementById('myModal');
    console.log('执行')
    closeModal(pdfModal)
}

var modalButtons = document.querySelectorAll("[data-modal-action]");

// 获取模态框主体
var modals = document.querySelectorAll(".modal");
// 打开模态框
function openModal(modal) {
    modal.style.display = "block";
    modal.querySelector(".modal-content").classList.remove("modal-hide");
}

// 关闭模态框
function closeModal(modal) {
    modal.querySelector(".modal-content").classList.add("modal-hide");
    modal.style.display = "none";
}

// 监听模态框的关闭时事件
modals.forEach(function(modal) {
    var closeButton = modal.querySelector(".close");
    if (closeButton) {
        closeButton.addEventListener("click", function() {
            var targetModal = this.closest(".modal");
            closeModal(targetModal);
        });
    }
});

// 当用户点击模态框外部时，关闭模态框
window.onclick = function (event) {
    modals.forEach(function(modal) {
        if (event.target === modal) {
            closeModal(modal);
        }
    });
};