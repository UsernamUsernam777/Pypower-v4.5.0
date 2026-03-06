import _datetime
import customtkinter as _ctk
import pyperclip as _pyperclip
import time as _time
import webbrowser as _webbrowser
import os as _os
import subprocess as _subprocess
import random as _random
class Time:
    def random_time(method=12, with_sec=True):
        if method == 12:
            hours = [n for n in range(1, 13)]
        else:
            hours = [n for n in range(24)]
        result = f"{_random.choice(hours):02}:{_random.randint(0, 59):02}"
        if with_sec:
            result += f':{_random.randint(0, 59):02}'
        return result
    def minus_clock(time_str1, time_str2):
        t1 = Time.reverse_many_hms(time_str1)
        t2 = Time.reverse_many_hms(time_str2)
        return Time.how_many_hms_in_s(abs(t1-t2))
    """convert time to type_output"""
    def convert_to_iterable_and_int(time_str, type_output=tuple):
        """Convert 'HH:MM:SS' string to an iterable of ints. ex: '01:30:45' -> (1, 30, 45)"""
        return type_output(map(int, time_str.split(':')))
    def how_many_hms_in_s(sec):
        """how many hours, minutes and seconds in seconds"""
        hours = sec // 3600
        minutes = (sec % 3600) // 60
        seconds = (sec % 3600) % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    def reverse_many_hms(time_str):
        result = Time.convert_to_iterable_and_int(time_str)
        return (result[0]*3600) + (result[1]*60) + result[2]
class Other:
    def copy_pypower(path):
        """Copy the contents of pypower.py to the clipboard."""
        with open(path, 'r', encoding='utf-8') as f:
            _pyperclip.copy(f.read())
    def search_google(text):
        """Open a new browser tab with a Google search for text."""
        _webbrowser.open_new_tab(f"https://www.google.com/search?q={text}&oq=&gs_lcrp=EgZjaHJvbWUqCQgAECMYJxjqAjIJCAAQIxgnGOoCMgkIARAjGCcY6gIyCQgCEEUYOxjCAzIRCAMQABgDGEIYjwEYtAIY6gIyDwgEEC4YAxiPARi0AhjqAjIRCAUQABgDGEIYjwEYtAIY6gIyEQgGEAAYAxhCGI8BGLQCGOoCMg8IBxAuGAMYjwEYtAIY6gLSAQg0MDVqMGoxNagCCLACAfEF1j7Fc7lEloM&sourceid=chrome&ie=UTF-8")
    def in_bg(name, duration, action=None):
        """Run action in a background thread after duration seconds.
don't write repeated name."""
        import threading as _threading
        names = [i.name for i in _threading.enumerate()]
        if name not in names:
            def v():
                _time.sleep(duration)
                if action:
                    action()
            a = _threading.Thread(name=name, target=v, daemon=True)
            a.start()
class Apps:
    def create_app(path, icon=None):
        """Build a standalone .exe from a .py file using PyInstaller, then clean up build files."""
        def mainloop():
            if not _os.path.exists(path):
                print('Error!')
            else:
                pj = _os.path.dirname(path)
                n_py = _os.path.basename(path)
                n_exe = _os.path.basename(path).replace('.py', '.exe')
                n_spec = _os.path.basename(path).replace('.py', '.spec')
                pro = ['pyinstaller', '--onefile', '--windowed', n_py]
                _os.chdir(pj)
                if icon:
                    pro.append(f'--icon={icon}')
                p = _subprocess.Popen(pro, creationflags=_subprocess.CREATE_NO_WINDOW)
                p.wait()
                if _os.path.exists(_os.path.join('dist', n_exe)):
                    _os.replace(_os.path.join('dist', n_exe), _os.path.join(pj, n_exe))
                if _os.path.exists(_os.path.join(pj, n_exe)):
                    _os.system('rmdir /s /q dist')
                    _os.system('rmdir /s /q build')
                    _os.remove(n_spec)
                if _os.path.exists(path.replace('.py', '.exe')):
                    print(f"App Created Successed in {path.replace('.py', '.exe')}")
        Other.in_bg(1, mainloop)
class Files:
    def make_if_not_exists(path, type=''):
        """Create a folder (type='') or empty file at path if it doesn't exist."""
        if not _os.path.exists(path):
            if type == '':
                _os.mkdir(path)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    pass
    def append_to_pypower(path, class_name, code):
        """Append a labeled code block to pypower.py."""
        Files.append_to_file(path, f'\n#{class_name}\n'+code)
    def append_to_file(path, text):
        """Append text to a file, removing double blank lines."""
        with open(path, 'r', encoding='utf-8') as a:
            old_text = a.read()
        with open(path, 'w', encoding='utf-8') as b:
            new_text = old_text + '\n' + text
            b.write(new_text.replace('\n\n', '\n'))
class GUI:
    class CustomTk:
        def sync_entry_with_label(entry, label):
            var = ctk.StringVar()
            var.trace_add('write', lambda *args:label.configure(text=entry.get()))
            entry.configure(textvariable=var)
        def console(master, texts, per_row=3, entry_to_insert=None, font=('arial', 20), text_color='white', return_dic_frame_and_buttons=False):
            result = _ctk.CTkFrame(master)
            def create_button(text):
                if entry_to_insert:
                    return _ctk.CTkButton(result, text=text, font=font, text_color=text_color, command=lambda: entry_to_insert.insert('end', text))
                return _ctk.CTkButton(result, text=text, font=font, text_color=text_color)
            buttons = [create_button(str(c)) for c in texts]
            GUI.CustomTk.tidy_up(buttons, per_row=per_row)
            if return_dic_frame_and_buttons:
                return {'frame': result, 'buttons': buttons}
            return result
        def console_num(master, per_row=3, entry_to_insert=None, font=('arial', 20), text_color='white'):
            return GUI.CustomTk.console(master, range(10), per_row, entry_to_insert, font=font, text_color=text_color)
        class Timer:
            def __init__(self, duration, obj, start_icon='start', stop_icon='stop', when_finish=None):
                self.duration = duration
                self.resume = self.duration > 0
                self.obj = obj
                self.button = _ctk.CTkButton(obj.master, text=start_icon, command=self.start)
                self.start_icon = start_icon
                self.stop_icon = stop_icon
                self.timers = 0
                self.when_finish = when_finish
                if self.when_finish and self.duration == 0:
                    self.when_finish()
            def start(self):
                self.button.configure(command=self.stop, text=self.stop_icon)
                def m():
                    while self.resume:
                        self.duration -= 1
                        self.obj.configure(text=Time.how_many_hms_in_s(self.duration))
                        _time.sleep(1)
                Other.in_bg(f'{id(self.obj)}', 0, m)
            def stop(self):
                self.button.configure(command=self.resume_timer, text=self.start_icon)
                self.resume = False
            def resume_timer(self):
                self.resume = self.duration > 0
                self.start()
        def show_hide_button(entry, show_ico="show", hide_ico='hide', hide_with="*"):
            entry.configure(show=hide_with)
            btn = _ctk.CTkButton(entry.master, text=show_ico, font=("arial", 20))
            def change():
                if entry.cget("show") == hide_with:
                    entry.configure(show='')
                    btn.configure(text=hide_ico)
                else:
                    entry.configure(show=hide_with)
                    btn.configure(text=show_ico)
            btn.configure(command=change)
            return btn
        def move(obj):
            master = obj.master
            master.update_idletasks()
            x = obj.winfo_x()
            y = obj.winfo_y()
            obj.pack_forget()
            obj.grid_forget()
            obj.place(x=x, y=y)
            width = obj.winfo_width()
            height = obj.winfo_height()
            obj.bind('<B1-Motion>', lambda e:obj.place(x=master.winfo_pointerx()-width//2, y=master.winfo_pointery()-height//2))
        def good_size(widgets):
            """resize widgets with the biggest size (height, width)"""
            def m():
                width = [i.winfo_reqwidth() for i in widgets]
                height = [i.winfo_reqheight() for i in widgets]
                for i in widgets:
                    i.configure(width=max(width), height=max(height))
            Other.in_bg('good size', 0, m)
        def tidy_up(widgets, per_row, start_from_row=0, start_from_column=0, distance_down=5, distance_across=5):
            def m():
                """
                Arrange widgets in a grid with a fixed number per row.
                """
                master = widgets[0].master
                for i in range(start_from_row+1):
                    master.grid_rowconfigure(i, minsize=widgets[0].winfo_reqheight())
                for i in range(start_from_column+1):
                    master.grid_columnconfigure(i, minsize=widgets[0].winfo_reqwidth())
                columns = start_from_column
                rows = start_from_row
                allowed_num = 0
                multy = Math.number_multiplies(per_row, len(widgets), set)
                for w in widgets:
                    w.grid(column=columns, row=rows, padx=distance_across, pady=distance_down)
                    allowed_num += 1
                    columns += 1
                    if allowed_num in multy:
                        rows += 1
                        columns = start_from_column
            Other.in_bg('tidy up func', len(widgets) // 1000, m)
        def all_objects(master):
            """Return a flat list of all child widgets in master."""
            result = []
            for i in master.winfo_children():
                if isinstance(i, (_ctk.CTkFrame, _ctk.CTkScrollableFrame)):
                    result.extend(all_objects(i))
                else:
                    result.append(i)
            return result
        def edit_all_widgets_texts(master, font='arial', size=20, text_color='lightblue', bg=''):
            """Apply font, text color, and background to all child widgets in master."""
            def m():
                for i in master.winfo_children():
                        if isinstance(i, (_ctk.CTkLabel, _ctk.CTkButton)):
                            if bg:
                                i.configure(font=(font, size), text_color=text_color, fg_color=bg)
                            else:
                                i.configure(font=(font, size), text_color=text_color, fg_color='transparent')
            Other.in_bg('edit_all_texts', 0.5, m)
        def info(widget, information, font='arial', size=20, bg='', hide_after=5):
            """Show a tooltip label below widget on hover, auto-hide after hide_after seconds."""
            if bg:
                inf = _ctk.CTkLabel(widget.master, text=information, font=(font, size), fg_color=bg)
            else:
                inf = _ctk.CTkLabel(widget.master, text=information, font=(font, size), fg_color=None)
            def show(e):
                x = widget.winfo_x()
                y = widget.winfo_y()
                inf.after(1000, lambda: inf.place(x=x, y=y+widget.winfo_height()))
                inf.after(hide_after*1000, inf.place_forget)
            widget.bind('<Enter>', show)
        def mouse_wheel_num(entry, start, end):
            """Scroll through numbers in range [start, end] inside an entry with the mouse wheel."""
            try:
                def f(e):
                    a = entry.get()
                    b = range(start, end+1)
                    if a.isdigit():
                        entry.delete(0, 'end')
                        if e.delta >= 1:
                            entry.insert(0, (b.index(int(a)) + 1) % len(b))
                        else:
                            entry.insert(0, (b.index(int(a)) - 1) % len(b))
                entry.bind("<MouseWheel>", f)
            except Exception as e:
                pass
    class Turtle:
        def in_circle(turtle_obj, shape_as_func, how_many=10):
            """draw shape_as_func in circle"""
            for i in range(how_many):
                shape_as_func()
                turtle_obj.left(360/how_many)
        def rock_bottom(window, obj, before_end=0):
            x = window.window_width() // 2 - before_end
            y = window.window_height() // 2 - before_end
            return abs(obj.xcor()) >= abs(x) or abs(obj.ycor()) >= abs(y)
        def move(obj, distance, direction='forward'):
            """Move a Turtle object without drawing (pen up then down)."""
            if direction in ['backward', 'forward']:
                obj.penup()
                if direction == 'forward':
                    obj.fd(distance)
                elif direction == 'backward':
                    obj.bk(distance)
                obj.pendown()
            else:
                print('Invalid direction!')
class String:
    def __init__(self, text):
        self.text = text
    def there_is_a_number(self , start=0, end=9):
        """Return True if the string contains any digit in range [start, end]."""
        a = ''
        for i in self.text:
            if i.isdigit():
                if int(i) in range(start, end+1):
                    a += i
        return bool(a)
    def super_join(self, sep, after_how_many_letters):
        """Insert sep every after_how_many_letters characters in the string."""
        value = 0
        new = ''
        ran = Math.number_multiplies(after_how_many_letters, len(self.text)-1)
        for i in self.text:
            new += i
            value += 1
            if value in ran:
                new += sep
        return new
    def reverse(self, sep):
        """Reverse the order of parts split by sep. ex: 'a-b-c' -> 'c-b-a'"""
        return f'{sep}'.join(self.text.split(sep)[::-1])
    def replace_objects_with_one(self, iterable, new_obj=''):
        """Replace every character found in iterable with new_obj."""
        result = ''
        for i in self.text:
            if i not in iterable:
                result += i
            else:
                result += new_obj
        return result
    def replace_many(self, old_iterable, new_iterable):
        """Replace each character in old_iterable with the matching one in new_iterable."""
        result = ''
        for i in self.text:
            if i in old_iterable:
                result += new_iterable[old_iterable.index(i)]
            else:
                result += i
        return result
    def between(self, c1, c2, include_c1_c2=True):
        """return string between two points"""
        index = [self.text.index(c1), self.text.index(c2)]
        if not include_c1_c2:
            index[0] = index[0]+ 1
            index[1] = index[1] - 1
        return self.text[index[0]:index[1]]
class Iterable:
    def search_iterable(iterable, search_with, ignore_case=True):
        result = []
        for o in iterable:
            if ignore_case:
                if str(search_with).lower() in str(o).lower():
                    result.append(o)
            else:
                if str(search_with) in str(o):
                    result.append(o)
        return result
    def get_circular_index(iterable, index, return_obj=False):
        """
    Return the element at 'index' using modulo to wrap around if index >= len(iterable).
    This creates a circular loop, preventing IndexError and allowing infinite cycling.
    Example: get_circular_index(['a', 'b'], 2) -> 'a'
    """
        i = index % len(iterable)
        if return_obj:
            return iterable[i]
        else:
            return i
    def any_is_class(iterable, clas, first_object_only=True):
        """
    Check for objects of a specific class in an iterable.

    Returns the first match if first_object_only is True (default). 
    Otherwise, returns a set of all matches for O(1) membership testing.
    """
        if first_object_only:
            for i in iterable:
                if isinstance(i, clas):
                    return i
            return []
        else:
            result = set()
            for i in iterable:
                if isinstance(i, clas):
                    result.add(i)
            return result if result else []
    def numred(iterable):
        """numred the objects in an iterable ex: if you want to create numred tasks
            numred(['visiting my uncle', 'water the plants'])  1.visiting my uncle"""
        result = ''
        for i in range(len(iterable)):
            result += f"{i+1}. {iterable[i]}\n"
        return result.strip()
    def return_brakets():
        """return the brakets in a dict"""
        return {'list': ('[', ']'), 'tuple':('(', ')'), 'curley': ('{', '}')}
    def replace_iterable(iterable, index, new_obj=None):
        """replace an object by it's index with new_obj ex:    replace(['mike', 'mark'], 1, 'Olivia')
result = ['Olivia', 'mark']"""
        co = iterable.copy()
        if new_obj:
            co[index-1] = new_obj
        else:
            co.remove(co[index-1])
        return co
    def all_in(main_iterable, iterable):
        """Checks if all unique elements of 'iterable' exist within 'main_iterable'."""
        for i in set(iterable):
            if i not in main_iterable:
                return False
        return True
    class Dict:
        def swap_dict(dic):
            """k: v ➡ v, k"""
            result = {}
            for k, v in dic.items():
                if isinstance(v, (list, tuple, set, dict)):
                    v = str(v)
                result[v] = k
            return result
    def return_dict_in_lines(dec):
        """Return a dict formatted as 'key: value' lines."""
        result = ''
        for i in dec:
            result += f"{i}: {dec[i]}\n"
        return result.strip()
class Math:
    def int_or_float(num):
        try:
            float(num)
            assert str(num)[-1] != '.'
            return True
        except:
            return False
    def iter_num(iterable):
        """Return sum, average, max, and min of an iterable as a dict."""
        return {'sum': sum(iterable), 'average': sum(iterable) / len(iterable), 'max': max(iterable), 'min': min(iterable)}
    def number_multiplies(num, end, type=list):
        """Return all multiples of num up to end. ex: number_multiplies(3, 9) -> [3, 6, 9]"""
        return type(range(num, end+1, num))
    def arrays(array, step, show='lists'):
        """Split a range into consecutive [start, end] pairs by step.
        If show != 'lists', return a formatted string instead."""
        result = []
        for i in range(step, array, step):
            result.append([i, i+step])
        if show != 'lists':
            result2 = ''
            for i, e in result:
                result2 += str((i, e)).replace('(', '').replace(')', '').replace(', ', ' - ')+'\n'
            return result2.strip()
        return result
