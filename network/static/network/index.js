document.addEventListener("DOMContentLoaded", () => {
    // handle edit function
    const edit_list = document.querySelectorAll('.fa-edit');
    // for each edit button assign a function reference to handle edit
    edit_list.forEach(button => {
        button.onclick = () => handleEdit(button);
    });

    // call like function
    const like_list = document.querySelectorAll('.fa-heart');
    like_list.forEach(button => {
        button.onclick = () => like_post(button);
    })

});

const handleEdit = button => {
    //fetch the post id and post body from the post
    button.style.display = 'none';
    const post_id = button.dataset.postid;
    const post_body_div = document.querySelector(`#post-no-${post_id}`).children[1];
    post_body_div.style.display = 'none';

    // Creating edit division
    const edit_area = document.createElement('div');
    edit_area.setAttribute("id", "edit-card");
    edit_area.style.padding = '5px'
    // Create text area to edit the post
    const text_area = document.createElement('textarea');
    text_area.className = "form-control";
    text_area.setAttribute("rows", "5");
    text_area.setAttribute("id", "edit-content")
    text_area.innerHTML = button.dataset.content;
    // Create submit button so that onclick the post is updated
    const submit_button = document.createElement('button');
    submit_button.setAttribute("type", "submit");
    submit_button.className = "btn btn-primary"
    submit_button.innerHTML = "Save";
    submit_button.style.float = "right";
    submit_button.style.marginTop = "5px";
    // append the edit area to the card container
    edit_area.append(text_area, submit_button);
    document.querySelector(`#post-no-${post_id}`).append(edit_area);

    // save button onclick event handler
    submit_button.onclick = () => {
        button.style.display = 'block';
        return update_post(post_id);
    }
};
// function to handle send post request to server and update the post in database
const update_post = (post_id) => {
    // fetch text in the text area
    const post_body = document.querySelector('#edit-content').value;
    // send http post request to backend(django) and send the post body as content
    fetch(`/savepost/${parseInt(post_id)}`, {
        method: "POST",
        body: JSON.stringify({
            content: post_body
        })
    }). then(response => response.json())
    .then(data => {
        if ("error" in data) {
            console.log(data);
            return location.reload();
        }
        //remove the edit area and add the updated body to card body
        document.querySelector('#edit-card').remove()
        document.querySelector(`#post-no-${post_id}`).querySelector(`h5`).innerHTML = data.updated_post.body;
        document.querySelector(`#post-no-${post_id}`).children[1].style.display = 'block';
    })
}

const like_post = (button) => {
    post_id = button.dataset.postid;
    console.log(post_id)
    fetch(`/likepost/${parseInt(post_id)}`)
    .then(response => response.json())
    .then(data => {
        const heart = document.querySelector(`#post-no-${post_id}`).querySelector('.fa-heart')
        heart.innerHTML = data.likers;
    })
}