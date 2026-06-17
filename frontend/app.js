const API_URL = window.location.origin;

const loginForm = document.getElementById("login-form");
const postForm = document.getElementById("post-form");
const loginMessage = document.getElementById("login-message");
const postMessage = document.getElementById("post-message");
const postsContainer = document.getElementById("posts");

const tokenKey = "blog_access_token";

function getToken() {
  return localStorage.getItem(tokenKey);
}

function saveToken(token) {
  localStorage.setItem(tokenKey, token);
}

async function fetchPosts() {
  const response = await fetch(`${API_URL}/posts/`);
  const posts = await response.json();
  postsContainer.innerHTML = "";
  posts.forEach((post) => {
    const postCard = document.createElement("div");
    postCard.className = "post-item";
    postCard.innerHTML = `
      <h3>${post.title}</h3>
      <p>${post.content}</p>
      <small>Author ID: ${post.author_id}</small>
    `;
    postsContainer.appendChild(postCard);
  });
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const body = new URLSearchParams();
  body.append("username", username);
  body.append("password", password);

  const response = await fetch(`${API_URL}/api/token`, {
    method: "POST",
    body,
  });

  if (!response.ok) {
    loginMessage.textContent = "Login failed. Check credentials.";
    return;
  }

  const data = await response.json();
  saveToken(data.access_token);
  loginMessage.textContent = "Login successful. You can now create posts.";
});

postForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const title = document.getElementById("post-title").value;
  const content = document.getElementById("post-content").value;
  const token = getToken();

  if (!token) {
    postMessage.textContent = "Please login first.";
    return;
  }

  const response = await fetch(`${API_URL}/posts/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title, content }),
  });

  if (!response.ok) {
    postMessage.textContent = "Unable to create post. Make sure you are logged in.";
    return;
  }

  postMessage.textContent = "Post created successfully.";
  document.getElementById("post-title").value = "";
  document.getElementById("post-content").value = "";
  fetchPosts();
});

fetchPosts();
