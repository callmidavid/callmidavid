import os
from datetime import datetime

import gitos
from zoneinfo import ZoneInfo

# Use absolute paths so fonts are found regardless of working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "fonts")

FONT_FILE_LOGO = os.path.join(FONT_DIR, "vtks-blocketo.regular.ttf")
# FONT_FILE_BITMAP = os.path.join(FONT_DIR, "ter-u14n.pil")
FONT_FILE_BITMAP = os.path.join(FONT_DIR, "gohufont-uni-14.pil")
FONT_FILE_TRUETYPE = os.path.join(FONT_DIR, "IosevkaTermNerdFont-Bold.ttf")
FONT_FILE_MONA = os.path.join(FONT_DIR, "Inversionz.otf")


def main():
    # Select a usable font file. Prefer project bitmap `.pil`, then TTFs
    # in the repo, then system truetype fonts. We require a minimum file
    # size to avoid placeholder files being used.
    def find_usable_font(candidates, min_size=2048):
        for p in candidates:
            try:
                if p and os.path.isfile(p) and os.path.getsize(p) >= min_size:
                    return p
            except Exception:
                continue
        return None

    candidates = [FONT_FILE_BITMAP, FONT_FILE_TRUETYPE, FONT_FILE_LOGO, FONT_FILE_MONA]
    bitmap_font_to_use = find_usable_font(candidates)

    # If none found in repo, try common system font locations
    if not bitmap_font_to_use:
        sys_font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
        ]
        bitmap_font_to_use = find_usable_font(sys_font_paths)

    if not bitmap_font_to_use:
        # Last resort: try any .ttf under /usr/share/fonts/truetype
        try:
            for root, dirs, files in os.walk("/usr/share/fonts/truetype"):
                for f in files:
                    if f.lower().endswith(".ttf"):
                        fp = os.path.join(root, f)
                        if os.path.getsize(fp) >= 2048:
                            bitmap_font_to_use = fp
                            break
                if bitmap_font_to_use:
                    break
        except Exception:
            bitmap_font_to_use = None

    if not bitmap_font_to_use:
        print("WARNING: No usable font found in project or system paths; gitos may fail to render correctly. Add real fonts to the `fonts/` folder.")
        bitmap_font_to_use = FONT_FILE_BITMAP

    t = gitos.Terminal(750, 500, 15, 15, bitmap_font_to_use, 15)

    t.gen_text("", 1, count=20)
    t.toggle_show_cursor(False)
    year_now = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y")
    t.gen_text("Kafy OS Modular BIOS v1.0.11", 1)
    t.gen_text(f"Copyright (C) {year_now}, \x1b[31mCallmidavid Softwares Inc.\x1b[0m", 2)
    t.gen_text("\x1b[94mGitHub Profile ReadMe Terminal, Rev 1011\x1b[0m", 4)
    t.gen_text("Krypton(tm) GIFCPU - 250Hz", 6)
    t.gen_text(
        "Press \x1b[94mDEL\x1b[0m to enter SETUP, \x1b[94mESC\x1b[0m to cancel Memory Test",
        t.num_rows,
    )
    for i in range(0, 65653, 7168):  # 64K Memory
        t.delete_row(7)
        if i < 30000:
            t.gen_text(
                f"Memory Test: {i}", 7, count=2, contin=True
            )  # slow down upto a point
        else:
            t.gen_text(f"Memory Test: {i}", 7, contin=True)
    t.delete_row(7)
    t.gen_text("Memory Test: 64KB OK", 7, count=10, contin=True)
    t.gen_text("", 11, count=10, contin=True)

    t.clear_frame()
    t.gen_text("Initiating Boot Sequence ", 1, contin=True)
    t.gen_typing_text(".....", 1, contin=True)
    t.gen_text("\x1b[96m", 1, count=0, contin=True)  # buffer to be removed
    t.set_font(FONT_FILE_LOGO, 66)
    # t.toggle_show_cursor(True)
    os_logo_text = "Kafy OS"
    mid_row = (t.num_rows + 1) // 2
    mid_col = (t.num_cols - len(os_logo_text) + 1) // 2
    effect_lines = gitos.effects.text_scramble_effect_lines(
        os_logo_text, 3, include_special=False
    )
    for i in range(len(effect_lines)):
        t.delete_row(mid_row + 1)
        t.gen_text(effect_lines[i], mid_row + 1, mid_col + 1)

    t.set_font(FONT_FILE_BITMAP, 15)
    t.clear_frame()
    t.clone_frame(5)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93mKafy OS v1.0.11 (tty1)\x1b[0m", 1, count=5)
    t.gen_text("login: ", 3, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("callmidavid", 3, contin=True)
    t.gen_text("", 4, count=5)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("*********", 4, contin=True)
    t.toggle_show_cursor(False)
    time_now = datetime.now(ZoneInfo("Asia/Kolkata")).strftime(
        "%a %b %d %I:%M:%S %p %Z %Y"
    )
    t.gen_text(f"Last login: {time_now} on tty1", 6)

    t.gen_prompt(7, count=5)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mclea", 7, contin=True)
    t.delete_row(7, prompt_col)  # simulate syntax highlighting
    t.gen_text("\x1b[92mclear\x1b[0m", 7, count=3, contin=True)

    ignore_repos = ["archiso-zfs", "archiso-zfs-archive"]
    git_user_details = gitos.utils.fetch_github_stats("callmidavid", ignore_repos)
    user_age = gitos.utils.calc_age(26, 7, 2002)
    t.clear_frame()
    top_languages = [lang[0] for lang in git_user_details.languages_sorted]
    user_details_lines = f"""
    \x1b[30;101mcallmidavid@GitHub\x1b[0m
    --------------
    \x1b[96mOS:     \x1b[93mKafy OS, Arch, Android 14\x1b[0m
    \x1b[96mHost:   \x1b[93mKingsley Ozumba Mbadiwe University \x1b[94m#NSEC\x1b[0m
    \x1b[96mKernel: \x1b[93mComputer Science \x1b[94m#CSE\x1b[0m
    \x1b[96mUptime: \x1b[93m{user_age.years} years, {user_age.months} months, {user_age.days} days\x1b[0m
    \x1b[96mIDE:    \x1b[93mneovim, VSCode\x1b[0m
    
    \x1b[30;101mContact:\x1b[0m
    --------------
    \x1b[96mEmail:      \x1b[93mdaviduchennamuna@gmail.com\x1b[0m
    \x1b[96mLinkedIn:   \x1b[93mking-dave\x1b[0m
    
    \x1b[30;101mGitHub Stats:\x1b[0m
    --------------
    \x1b[96mUser Rating: \x1b[93m{git_user_details.user_rank.level}\x1b[0m
    \x1b[96mTotal Stars Earned: \x1b[93m{git_user_details.total_stargazers}\x1b[0m
    \x1b[96mTotal Commits ({int(year_now) - 1}): \x1b[93m{git_user_details.total_commits_last_year}\x1b[0m
    \x1b[96mTotal PRs: \x1b[93m{git_user_details.total_pull_requests_made}\x1b[0m
    \x1b[96mMerged PR %: \x1b[93m{git_user_details.pull_requests_merge_percentage}\x1b[0m
    \x1b[96mTotal Contributions: \x1b[93m{git_user_details.total_repo_contributions}\x1b[0m
    \x1b[96mTop Languages: \x1b[93m{', '.join(top_languages[:5])}\x1b[0m
    """
    t.gen_prompt(1)
    prompt_col = t.curr_col
    t.clone_frame(10)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(" -u callmidavid", 1, contin=True)

    t.set_font(FONT_FILE_MONA, 16, 0)
    t.toggle_show_cursor(False)
    monaLines = r"""
    \x1b[49m     \x1b[90;100m}}\x1b[49m     \x1b[90;100m}}\x1b[0m
    \x1b[49m    \x1b[90;100m}}}}\x1b[49m   \x1b[90;100m}}}}\x1b[0m
    \x1b[49m    \x1b[90;100m}}}}}\x1b[49m \x1b[90;100m}}}}}\x1b[0m
    \x1b[49m   \x1b[90;100m}}}}}}}}}}}}}\x1b[0m
    \x1b[49m   \x1b[90;100m}}}}}}}}}}}}}}\x1b[0m
    \x1b[49m   \x1b[90;100m}}\x1b[37;47m}}}}}}}\x1b[90;100m}}}}}\x1b[0m
    \x1b[49m  \x1b[90;100m}}\x1b[37;47m}}}}}}}}}\x1b[90;100m}}}\x1b[0m
    \x1b[49m  \x1b[90;100m}}\x1b[37;47m}\x1b[90;100m}\x1b[37;47m}}}}}\x1b[90;100m}\x1b[37;47m}}\x1b[90;100m}}}}\x1b[0m
    \x1b[49m  \x1b[90;100m}\x1b[37;47m}}\x1b[90;100m}\x1b[37;47m}}}}}\x1b[90;100m}\x1b[37;47m}}}\x1b[90;100m}}}\x1b[0m
    \x1b[90;100m}}}\x1b[37;47m}}}}\x1b[90;100m}}}\x1b[37;47m}}}}}\x1b[90;100m}}}}\x1b[0m
    \x1b[49m  \x1b[90;100m}\x1b[37;47m}}}}}\x1b[90;100m}}\x1b[37;47m}}}}}\x1b[90;100m}}}\x1b[0m
    \x1b[49m \x1b[90;100m}}\x1b[37;47m}}}}}}}}}}}\x1b[90;100m}}}\x1b[0m
    \x1b[90;100m}\x1b[49m  \x1b[90;100m}}\x1b[37;47m}}}}}}}\x1b[90;100m}}}\x1b[49m  \x1b[90;100m}\x1b[0m
    \x1b[49m        \x1b[90;100m}}}}}\x1b[0m
    \x1b[49m       \x1b[90;100m}}}}}}}\x1b[0m
    \x1b[49m       \x1b[90;100m}}}}}}}}\x1b[0m
    \x1b[49m      \x1b[90;100m}}}}}}}}}}\x1b[0m
    \x1b[49m     \x1b[90;100m}}}}}}}}}}}\x1b[0m
    \x1b[49m     \x1b[90;100m}}}}}}}}}}}}\x1b[0m
    \x1b[49m     \x1b[90;100m}}\x1b[49m \x1b[90;100m}}}}}}\x1b[49m \x1b[90;100m}}\x1b[0m
    \x1b[49m        \x1b[90;100m}}}}}}}\x1b[0m
    \x1b[49m         \x1b[90;100m}}}\x1b[49m \x1b[90;100m}}\x1b[0m
    """
    t.gen_text(monaLines, 10)

    t.set_font(FONT_FILE_BITMAP)
    t.toggle_show_cursor(True)
    # t.pasteImage("./temp/callmidavid.jpg", 3, 5, sizeMulti=0.5)
    t.gen_text(user_details_lines, 2, 35, count=5, contin=True)
    t.gen_prompt(t.curr_row)
    t.gen_typing_text(
        "\x1b[92m# Have a nice day kind stranger :D Thanks for stopping by!",
        t.curr_row,
        contin=True,
    )
    # t.save_frame("fetch_details.png")
    t.gen_text("", t.curr_row, count=120, contin=True)

    t.gen_gif()
    # image = gitos.utils.upload_imgbb("output.gif", 129600)  # 1.5 days expiration
    readme_file_content = rf"""<div align="justify">
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="./output.gif">
    <source media="(prefers-color-scheme: light)" srcset="./output.gif">
    <img alt="GITOS" src="output.gif">
</picture>

<sub><i>Generated automatically using [callmidavid/gitos](https://github.com/callmidavid/gitos) on {time_now}</i></sub>

<!-- <details>
<summary>More details</summary>

</details> -->
</div>

<!-- Image deletion URL: NONE -->"""
    with open("README.md", "w") as f:
        f.write(readme_file_content)
        print("INFO: README.md file generated")


if __name__ == "__main__":
    main()
