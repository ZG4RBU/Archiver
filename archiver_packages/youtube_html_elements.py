

def mention(text:str) -> str:
    mention = f'<span style="color: #3EA6FF;">{text}</span>'
    return mention


def redirect_url(text:str,url:str) -> str:
    timestamp = f'<a href="{url}"><span style="color: #3EA6FF;">{text}</span></a>'
    return timestamp


def text_url_style(text:str) -> str:
    timestamp = f'<a href="{text}"><span style="color: #3EA6FF;">{text}</span></a>'
    return timestamp


def heart(profile_image) -> str:
    heart=f"""
                <div class="channel-owner-reaction">
                  <img src="{profile_image}" alt="Channel owner reaction">
                  <div class="heart-reaction-border">
                    <svg viewBox="0 0 24 24" preserveAspectRatio="xMidYMid meet" focusable="false"><g>
                      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" class="heart-icon-border"></path>
                    </g></svg>
                  </div>
                  <div class="heart-reaction-icon">
                    <svg viewBox="0 0 24 24" preserveAspectRatio="xMidYMid meet" focusable="false"><g>
                      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" class="heart-icon"></path>
                    </g></svg>
                  </div>
                </div>
                """
    return heart


def comment_box(channel_url,channel_pfp,channel_username,channel_author,comment_date,text,like_count,heart,is_comment_pinned:bool) -> str:

    if is_comment_pinned:
        comment_pinned_element = f"""
              <div class="comment-pinned">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" style="pointer-events: none; display: inherit;">
                  <path d="M16 11V3h1V2H7v1h1v8l-2 2v2h5v6l1 1 1-1v-6h5v-2l-2-2zm1 3H7v-.59l1.71-1.71.29-.29V3h6v8.41l.29.29L17 13.41V14z" fill="#ffffff"></path>
                </svg>
                <span>Pinned by {channel_author}</span>
              </div>
              """
    else:
        comment_pinned_element = ""

    comment_box = f"""
          <div class="comment">
            <a href="{channel_url}"><div class="user-icons user-icon1"><img src="{channel_pfp}" alt="Avatar"></div></a>
              
            <div class="user">
              {comment_pinned_element}
              <a href="{channel_url}"><span class="user-name">{channel_username}</span><span class="date">{comment_date}</span></a>
              <span class="comment-text">{text}</span>
              
              <div class="user-comments-buttons">
                <button><i class='bx bx-like icon'></i></button>

                <span class="like">{like_count}</span>

                <button><i class='bx bx-dislike icon'></i></button>
                {heart}
                <button><span class="reply">Reply</span></button>
              </div>
            """
    return comment_box


def reply_box(channel_url,channel_pfp,channel_username,comment_date,text,like_count,heart) -> str:

    reply_box = f"""
          <div class="comment" style="position:relative; left:80px;">
            <a href="{channel_url}"><div class="user-icons user-icon1"><img src="{channel_pfp}" alt="Avatar"></div></a>
              
            <div class="user">
              <a href="{channel_url}"><span class="user-name">{channel_username}</span><span class="date">{comment_date}</span></a>
              <span class="comment-text">{text}</span>
              
              <div class="user-comments-buttons">
                <button><i class='bx bx-like icon'></i></button>

                <span class="like">{like_count}</span>

                <button><i class='bx bx-dislike icon'></i></button>
                {heart}
                <button><span class="reply">Reply</span></button>
              </div>
            </div>
          </div>
                    """
    return reply_box


def replies_toggle(reply_count) -> str:
    replies_toggle= f"""
              <button class="view-replies">
                <i class='bx bx-caret-down reply-icon'></i>
                <span>{reply_count}</span>
              </button>
                """
    return replies_toggle


class ending:
    divs = """
            </div>
          </div>
            """

    html_end = """
        </section>
      </section>

      <!-- Right Main Section -->
      <aside class="right-main-section">
        <section class="chat-section">
          <button class="chat-button">SHOW CHAT REPLAY</button>

          <ul class="button-label-cont">
            <li><button class="button-label" id="selected-item">All</button></li>
            <li><button class="button-label">Recently uploaded</button></li>
            <li><button class="button-label">Related</button></li>
            <li><button><i class='bx bx-chevron-right chevron-icon'></i></button></li>
          </ul>
        </section>

      </aside>
    </main>
  </body>
</html>
"""