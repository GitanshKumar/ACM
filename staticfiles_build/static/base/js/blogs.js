const csrf_token = document.querySelector('input[name=csrfmiddlewaretoken]').value;
var updatingLike = false
var timeout;

function updateLikeCount(byte, liked) {
    clearTimeout(timeout);

    timeout = setTimeout( function () {
        $.ajax({
            url: '/updatelikecountforbyte/' + byte.dataset.id + '/',
            method: 'POST',
            data: {'csrfmiddlewaretoken': csrf_token, 'liked':liked},
            success: function(data) {
                var likeCount = data.like_count;
                
                byte.querySelector(".count").innerText = likeCount;
            }
        })
    },
        400 * 5
    )
}

const likeBtn = document.querySelectorAll(".left .blog .likes");
likeBtn.forEach((btn) => {
    btn.addEventListener("click", function() {
        heart = btn.querySelector("i");
        if (heart.classList.contains("fa-heart-o")) {
            updateLikeCount(btn, true);
            heart.classList.replace("fa-heart-o", "fa-heart");
            return;
        }
        updateLikeCount(btn, false);
        heart.classList.replace("fa-heart", "fa-heart-o");
    })
})

const shareBtn = document.querySelectorAll(".left .blog .share");

shareBtn.forEach((btn) => {
    btn.addEventListener("click", async function() {
        var shareLink = btn.querySelector("input");

        shareLink.select();
        shareLink.setSelectionRange(0, 99999);

        try {
            await navigator.clipboard.writeText(shareLink.value);
            alert("Link Copied Successfully!");
        } catch (error) {
            console.error("Copy to clipboard failed: ", error);
            alert("Copy to clipboard failed. Please copy the link manually.");
        }
    });
})

const uploadBtn = document.querySelector(".submit.upload");
const submitForm = document.querySelector(".submit-container")

if (uploadBtn) {
    uploadBtn.addEventListener("click", function() {
        submitForm.classList.add("active");
    })
}

submitForm.addEventListener("click", function(event) {
    if (event.target == submitForm) {
        submitForm.classList.remove("active");
    }
})