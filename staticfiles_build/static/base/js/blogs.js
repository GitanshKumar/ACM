var remaining = true;
var loadingByte = false
var page = 2;


function loadMoreBytes() {
    loadingByte = true;
    $.ajax({
        url: '/loadmorebytes/',
        method: 'GET',
        data: {'page': page},
        success: function(data) {
            console.log(data);
            const bytes = data["bytes"];
            const owners = data["owners"];
            if (bytes.length == 0) {remaining = false;return;}
            
            const container = $("#bytes-container");

            for (var i = 0; i < bytes.length; i++) {
                const byte = bytes[i];
                const owner = owners[i];
                var child = `
                        <div class="blog">
                        <div class="blog-title-container">
                            <div class="owner">
                                <a href='/profile/${owner['username']}'>
                                    <div class="owner-pic">
                                        <img src="${owner['profile_pic']}" alt="">
                                    </div>
                                </a>
                                <div class="name">
                                    ${owner['name']}<br>
                                    <small>${owner['username']}</small>
                                </div>
                            </div>
                            <div class="date">${byte['created']}</div>
                        </div>
                        <a href="/blogs/${byte['id']}">
                            <div class="poster-container">
                                <img src="${byte['poster']}" alt="">
                            </div>
                        </a>
                        <div class="action-icons">
                            <div class="likes" data-id="${byte['id']}">
                                <i class="fa fa-heart${byte['liked'] ? '' : '-o'}" aria-hidden="true"></i>
                                <div class="count">${byte['likes']}</div>
                            </div>
                            <div class="comments">
                                <i class="fa fa-comment-o" aria-hidden="true"></i>
                            </div>
                            <div class="share">
                                <input type="text" value="/blogs/${byte['id']}" style="display: none;">
                                <i class="fa fa-share" aria-hidden="true"></i>
                            </div>
                            <div class="options">
                                <i class="fa fa-ellipsis-v" style="width: 20px;text-align: center;" aria-hidden="true"></i>
                            </div>
                        </div>
                        <div class="blog-caption-container">
                            <div class="caption">${byte['byte']}</div>
                        </div>
                    </div>
                `;

                container.append(child);
            }
            addListenerToActionIcons();
            loadingByte = false;
            page += 1;
        }
    })
}

const uploadBtn = document.querySelector(".submit.upload");
const submitForm = document.querySelector(".submit-container")

if (uploadBtn) {
    uploadBtn.addEventListener("click", function() {
        submitForm.classList.add("active");
    })
}
if (submitForm) {
    submitForm.addEventListener("click", function(event) {
        if (event.target == submitForm) {
            submitForm.classList.remove("active");
        }
    })
}


window.onscroll = function() {
    const bodyScrollHeight = document.body.scrollHeight;
    const windowHeight = window.innerHeight;
    const currentScroll = window.scrollY;
    
    const remainingScrollHeight = bodyScrollHeight - (currentScroll + windowHeight);

    if (remainingScrollHeight <= windowHeight && !loadingByte && remaining) {
        loadMoreBytes();
    }
}