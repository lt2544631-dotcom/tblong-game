import random
import time
import streamlit as st

# --- CẤU HÌNH TRÒ CHƠI ---
PAGE_WIDTH = 400
PAGE_HEIGHT = 600
PLAYER_SIZE = 40
OBSTACLE_SIZE = 50
GAME_SPEED = 0.05  # Tốc độ làm mới khung hình

# --- KHỞI TẠO TRẠNG THÁI ---
if "player_y" not in st.session_state:
  st.session_state.player_y = PAGE_HEIGHT // 2
if "score" not in st.session_state:
  st.session_state.score = 0
if "obstacles" not in st.session_state:
  st.session_state.obstacles = []
if "game_over" not in st.session_state:
  st.session_state.game_over = False


def create_obstacle():
  gap_y = random.randint(100, PAGE_HEIGHT - 100)
  st.session_state.obstacles.append({
      "x": PAGE_WIDTH,
      "y": 0,
      "height": gap_y - (OBSTACLE_SIZE // 2),
      "passed": False,
  })
  st.session_state.obstacles.append({
      "x": PAGE_WIDTH,
      "y": gap_y + (OBSTACLE_SIZE // 2),
      "height": PAGE_HEIGHT - gap_y - (OBSTACLE_SIZE // 2),
      "passed": False,
  })


def update_game_state():
  if not st.session_state.game_over:
    # Nhân vật di chuyển lên khi bấm nhảy
    st.session_state.player_y -= 12
    if st.session_state.player_y < 0:
      st.session_state.player_y = 0

    # Di chuyển rào cản
    for obstacle in st.session_state.obstacles:
      obstacle["x"] -= 10
      # Kiểm tra va chạm
      if obstacle["y"] == 0:
        if (
            obstacle["x"] < PAGE_WIDTH // 2 + PLAYER_SIZE
            and obstacle["x"] + OBSTACLE_SIZE > PAGE_WIDTH // 2
            and st.session_state.player_y < obstacle["height"]
        ):
          st.session_state.game_over = True
      else:
        if (
            obstacle["x"] < PAGE_WIDTH // 2 + PLAYER_SIZE
            and obstacle["x"] + OBSTACLE_SIZE > PAGE_WIDTH // 2
            and st.session_state.player_y + PLAYER_SIZE > obstacle["y"]
        ):
          st.session_state.game_over = True

      # Cộng điểm
      if not obstacle["passed"] and obstacle["x"] < PAGE_WIDTH // 2:
        obstacle["passed"] = True
        st.session_state.score += 0.5

    # Xóa rào cản cũ, tạo rào cản mới
    st.session_state.obstacles = [
        ob for ob in st.session_state.obstacles if ob["x"] > -OBSTACLE_SIZE
    ]
    if len(st.session_state.obstacles) < 6:
      create_obstacle()


# --- GIAO DIỆN TRÒ CHƠI ---
st.title("🏃‍♂️ Trò chơi Nhảy Phản Xạ")
st.write("Nhấn nút **Jump** liên tục để né chướng ngại vật!")

game_area = st.empty()


def draw_game():
  game_content = ""
  for obstacle in st.session_state.obstacles:
    game_content += (
        f'<div style="position: absolute; left: {obstacle["x"]}px; top:'
        f' {obstacle["y"]}px; width: {OBSTACLE_SIZE}px; height:'
        f' {obstacle["height"]}px; background-color: #f14; border: 2px solid'
        ' white;"></div>'
    )

  game_content += (
      f'<div style="position: absolute; left: {PAGE_WIDTH // 2}px; top:'
      f' {st.session_state.player_y}px; font-size: 32px; z-index: 10;">🏃</div>'
  )
  game_content += (
      f'<div style="position: absolute; top: 10px; right: 10px; color: white;'
      f' font-size: 24px; font-weight: bold;">Điểm:'
      f" {int(st.session_state.score)}</div>"
  )

  if st.session_state.game_over:
    game_content += (
        f'<div style="position: absolute; top: {PAGE_HEIGHT // 2}px; left:'
        f" {PAGE_WIDTH // 2 - 80}px; color: yellow; font-size: 35px; font-weight:"
        ' bold;">GAME OVER</div>'

    html_code = f"""
    <div style="position: relative; width: {PAGE_WIDTH}px; height: {PAGE_HEIGHT}px; background-color: #333; overflow: hidden; border: 5px solid white;">
        {game_content}
    </div>
    """
  game_area.markdown(html_code, unsafe_allow_html=True)


# Nút điều khiển
jump_button = st.button("🚀 Jump (Nhảy)", key="jump_btn")

if not st.session_state.obstacles:
  create_obstacle()

if jump_button:
  if st.session_state.game_over:
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.obstacles = []
  st.session_state.player_y -= 45  # Lực đẩy nhân vật bay lên khi bấm
  if st.session_state.player_y < 0:
    st.session_state.player_y = 0
  st.rerun()

# Vòng lặp cập nhật tự động
if not st.session_state.game_over:
  update_game_state()
  draw_game()
  time.sleep(GAME_SPEED)
  st.rerun()
else:
  draw_game()
  if st.button("Chơi lại"):
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.player_y = PAGE_HEIGHT // 2
    st.session_state.obstacles = []
    create_obstacle()
    st.rerun()
