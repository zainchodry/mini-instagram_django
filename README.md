# Mini Instagram

A simplified Instagram-like web app built with Django and Django Channels.  
It supports user accounts, posts (with images and captions), likes, comments, follow/unfollow, and real-time WebSocket notifications.

---

##  Features

### App 1: Accounts & Profiles
- User registration, login, logout
- Profile pages with avatar, bio, followers & following counts
- Edit profile with avatar upload
- Following / Unfollowing other users
- Search users

### App 2: Posts
- Create posts (image + caption)
- Feed with pagination
- Post detail view with likes and comments
- Like/unlike posts (with AJAX fallback)
- Comment on posts, delete own comments
- Admin interface for managing posts and comments

### App 3: Real-time Notifications (Django Channels)
- Notify users when someone likes, comments, or follows them
- Stores notifications in DB with read/unread status
- Real-time WebSocket updates via dropdown and notifications page
- Includes message dropdown and list UI

---

##  Getting Started

### Prerequisites
- Python 3.8+
- (Optional) Redis for Channels backend
- Virtual environment tool (recommended: `venv`, `virtualenv`)

### Installation

1. Clone project:
   ```bash
   git clone <mini_instagram_django>
   cd mini-instagram_django
