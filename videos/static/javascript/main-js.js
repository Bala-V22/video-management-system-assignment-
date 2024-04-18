function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('search-button').addEventListener('click', function () {
        searchVideos();
    });
});

function searchVideos() {
    var searchQuery = document.getElementById('search-input').value;
    fetch('/api/videos/search/?query=' + encodeURIComponent(searchQuery))
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data);
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
        });
}

function displaySearchResults(videos) {
    var cont = document.getElementById('video')
    var searchResultsDiv = document.getElementById('search-results');
    searchResultsDiv.innerHTML = ''; 
    cont.style.display='none'
    searchResultsDiv.style.display = 'block'

    videos.forEach(function (video) {
        var videoName = video.name;
        var videoUrl = video.url;
        var videoLink = document.createElement('a');
        videoLink.href = '#';
        videoLink.textContent = videoName;
        videoLink.onclick = function () {
            playVideo(videoUrl);
        };
        var videoElement = document.createElement('p');
        videoElement.appendChild(videoLink);
        searchResultsDiv.appendChild(videoElement);
    });
}


function setModalValue(name,id) {
    document.getElementById('name').value = name;
    document.getElementById('form-url').action = 'api/videos/edit/'+id+'/';
}

function playVideo(videoUrl) {
    window.location.href = '/play-video/' + videoUrl;
}



function deleteVideo(videoId) {
        if (confirm('Are you sure you want to delete this video?')) {
            $.ajax({
                url: '/api/videos/delete/' + videoId + '/',
                type: 'DELETE',
                headers: { 'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() },
                success: function(response) {
                    window.location.reload(); 
                },
                error: function(error) {
                    console.error('Error deleting video:', error);
                    alert('Failed to delete video');
                }
            });
        }
    }

document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/user/profile/")
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch user profile");
            }
            return response.json();
        })
        .then(data => {
            const userProfileDiv = document.getElementById("user-profile");
            userProfileDiv.innerHTML = `
                <h2>User Profile</h2>
                <p>Username: ${data.username}</p>
                <p>Email: ${data.email}</p>
                <!-- Add other profile fields as needed -->
            `;
        })
        .catch(error => {
            console.error("Error fetching user profile:", error);
            const userProfileDiv = document.getElementById("user-profile");
            userProfileDiv.innerHTML = "<p>Failed to fetch user profile. Please try again later.</p>";
        });
});