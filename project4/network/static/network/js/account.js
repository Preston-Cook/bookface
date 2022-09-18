document.addEventListener("DOMContentLoaded", () => {

    // Add event listeners to all save changes buttons
    document.querySelectorAll('.btn.btn-primary.save').forEach((btn) => {
        btn.onclick = () => {
            const text_element = document.querySelector('textarea');
            const text = text_element.value;
            const post_id = btn.dataset.postId;
            const div = document.createElement('div');

            fetch(`/edit/${post_id}`, {
                method: "PUT",
                body: JSON.stringify({
                    body: text
                })
            })

            div.setAttribute('id', `body-${post_id}`);
            div.setAttribute('class', 'post-body');
            div.innerHTML = text;

            text_element.replaceWith(div);

            btn.style.display = 'none';
            document.querySelector(`#discard-${post_id}`).style.display = 'none';
        }
    })

    // Add event listeners to all discard changes buttons
    document.querySelectorAll('.btn.btn-primary.discard').forEach((btn) => {
        btn.onclick = () => {
            const text_element = document.querySelector('textarea');
            const text = text_element.value;
            const post_id = btn.dataset.postId;
            const div = document.createElement('div');

            fetch(`/info/${post_id}`)
            .then(response => response.json())
            .then(post_data => {
                
                const prev_body = post_data["body"];
                div.setAttribute('id', `body-${post_id}`);
                div.setAttribute('class', 'post-body');
                div.innerHTML = prev_body;
                text_element.replaceWith(div);

                btn.style.display = 'none';
                document.querySelector(`#save-${post_id}`).style.display = 'none';
            })
        }
    })

    // Add event listeners to all edit buttons
    document.querySelectorAll('.btn.btn-primary.edit').forEach((btn) => {
        btn.onclick = () => {
            const post_id = btn.dataset.postId;
            const post_body = document.querySelector(`#body-${post_id}`);
            const post_content = post_body.innerHTML;

            let textarea = document.createElement('textarea');
            textarea.setAttribute('class', 'form-control');
            textarea.setAttribute('rows', "15");
            textarea.value = post_content;
            post_body.replaceWith(textarea);

            document.querySelector(`#save-${post_id}`).style.display = 'inline-block';
            document.querySelector(`#discard-${post_id}`).style.display = 'inline-block';
        }
    })

    // Add event listeners to all delete buttons
    document.querySelectorAll('.fa-solid.fa-trash.fa-lg').forEach((btn) => {
        btn.onclick = () => {
            const post_id = btn.dataset.postId;
            const div = document.querySelector(`#container-${post_id}`);

            fetch(`/delete/${post_id}`, {
                method: "DELETE",
                body: JSON.stringify({
                    post_id: post_id 
                })
            })

            div.parentNode.removeChild(div);
            document.querySelector('#delete-msg').style.display = 'block';
        }
    })

    // Add event listener to like buttons
    document.querySelectorAll('.fa.fa-thumbs-up.fa-lg').forEach((elm) => {
        elm.onclick = () => {
            const post_id = elm.dataset.postId;
            let like_count = parseInt(elm.innerHTML.slice(6));

            if (elm.style.color === "rgb(230, 75, 60)") {
                like_count--;
                elm.style.color = "black";
            }
            else {
                like_count++;
                elm.style.color = "rgb(230, 75, 60)";
            }

            fetch(`/like/${post_id}`, {
                method: "PUT",
                body: JSON.stringify({
                    likes: like_count
                })
            })

            elm.innerHTML = `&nbsp;${like_count}`;
        }
    })

    // Add event listener to follow button
    document.querySelector('#follow').onclick = follow;
})

function follow() {
    const text = this.innerHTML;
    const username = this.dataset.username;
    const follower_elm = document.querySelector('#followers');
    let follower_count = parseInt(follower_elm.innerHTML.slice(11));

    follower_elm.innerHTML = this.innerHTML === "Follow" ? `Followers: ${follower_count + 1}` : `Followers: ${follower_count - 1}`;
    this.innerHTML = this.innerHTML === "Follow" ? "Unfollow" : "Follow";
    
    fetch(`/follow/${username}`, {
        method: "PUT",
        body: JSON.stringify({
            follow: (text === "Follow")
        })
    })
}