// Function that runs once the window is fully loaded
window.onload = function() {
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Helper function to dynamically render posts (Used by loadPosts and searchPosts)
function renderPosts(data) {
    const postContainer = document.getElementById('post-container');
    postContainer.innerHTML = '';

    const searchTerm = document.getElementById('search-term') ? document.getElementById('search-term').value.trim() : '';

    if (data.length === 0 && searchTerm !== '') {
        postContainer.innerHTML = '<p class="no-results">No posts found matching your search term.</p>';
        return;
    } else if (data.length === 0) {
        postContainer.innerHTML = '<p class="no-results">No posts available. Add a new post above!</p>';
        return;
    }

    data.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.className = 'post';
        postDiv.id = `post-${post.id}`; // Add ID for easy manipulation during edit

        // Escape single quotes for safe use in JavaScript function call
        const safeTitle = post.title.replace(/'/g, "\\'");
        const safeContent = post.content.replace(/'/g, "\\'");

        postDiv.innerHTML = `
            <h2 id="title-${post.id}">${post.title}</h2>
            <p id="content-${post.id}">${post.content}</p>
            <div class="post-actions">
                <button class="edit-btn" onclick="editPost(${post.id}, '${safeTitle}', '${safeContent}')">Edit</button>
                <button class="delete-btn" onclick="deletePost(${post.id})">Delete</button>
            </div>
        `;
        postContainer.appendChild(postDiv);
    });
}

// Function to fetch all the posts with optional sorting
function loadPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    // Get sorting selections safely
    const sortFieldSelect = document.getElementById('sort-field');
    const sortDirectionSelect = document.getElementById('sort-direction');

    let url = baseUrl + '/posts';

    // Construct the URL with sorting query parameters if a sort field is selected
    if (sortFieldSelect && sortDirectionSelect && sortFieldSelect.value) {
        const sortField = sortFieldSelect.value;
        const sortDirection = sortDirectionSelect.value;
        url += `?sort=${sortField}&direction=${sortDirection}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { 
                    alert(`Error loading posts: ${err.error}`);
                    throw new Error(err.error); 
                });
            }
            return response.json();
        })
        .then(data => {
            renderPosts(data);
        })
        .catch(error => console.error('Error fetching posts:', error));
}

// Function to send a POST request to add a new post
function addPost() {
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value.trim();
    var postContent = document.getElementById('post-content').value.trim();

    if (!postTitle || !postContent) {
        alert("Title and Content cannot be empty.");
        return;
    }

    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent })
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to add post');
        return response.json();
    })
    .then(post => {
        console.log('Post added:', post);
        document.getElementById('post-title').value = '';
        document.getElementById('post-content').value = '';
        loadPosts();
    })
    .catch(error => console.error('Error adding post:', error));
}

// Function to send a DELETE request to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.status === 200) {
            console.log('Post deleted:', postId);
            loadPosts();
        } else {
             alert("Error deleting post.");
        }
    })
    .catch(error => console.error('Error deleting post:', error));
}

// Function to handle the search request
function searchPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    var searchTerm = document.getElementById('search-term').value.trim();
    
    if (!searchTerm) {
        loadPosts();
        return;
    }
    
    const encodedTerm = encodeURIComponent(searchTerm);
    // Search against BOTH title and content fields simultaneously
    const searchUrl = `${baseUrl}/posts/search?title=${encodedTerm}&content=${encodedTerm}`;

    fetch(searchUrl)
        .then(response => response.json())
        .then(data => {
            renderPosts(data);
        })
        .catch(error => console.error('Error during search:', error));
}


// Function to toggle edit mode for a specific post
function editPost(postId, currentTitle, currentContent) {
    const postDiv = document.getElementById(`post-${postId}`);
    if (!postDiv) return;

    // Remove escaping from the content passed in the function call
    const cleanTitle = currentTitle.replace(/\\'/g, "'");
    const cleanContent = currentContent.replace(/\\'/g, "'");

    // Replace the post content with input fields and save/cancel buttons
    postDiv.innerHTML = `
        <div class="edit-mode">
            <input type="text" id="edit-title-${postId}" value="${cleanTitle}" class="edit-input">
            <textarea id="edit-content-${postId}" class="edit-input">${cleanContent}</textarea>
            <div class="edit-actions">
                <button class="update-btn" onclick="updatePost(${postId})">Save</button>
                <button class="cancel-btn" onclick="loadPosts()">Cancel</button>
            </div>
        </div>
    `;
}

// Function to send the PUT request to update a post
function updatePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;
    const newTitle = document.getElementById(`edit-title-${postId}`).value.trim();
    const newContent = document.getElementById(`edit-content-${postId}`).value.trim();

    if (!newTitle || !newContent) {
        alert("Title and Content cannot be empty during update.");
        return;
    }

    fetch(baseUrl + '/posts/' + postId, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTitle, content: newContent })
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to update post');
        return response.json();
    })
    .then(post => {
        console.log('Post updated:', post);
        loadPosts(); // Reload the posts to display the updated content and exit edit mode
    })
    .catch(error => console.error('Error updating post:', error));
}