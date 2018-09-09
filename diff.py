import difflib
import html


def get_diffs(a, b):
    fromlines = a.splitlines(keepends=False)
    tolines = b.splitlines(keepends=False)
    context_lines = None
    diffs = difflib._mdiff(
        fromlines,
        tolines,
        context_lines,
        linejunk=None,
        charjunk=difflib.IS_CHARACTER_JUNK
    )
    return list(diffs)


def diff_formatter(diffs):
    for ((left_no, left_line), (right_no, right_line), change) in diffs:
        if change:
            if left_no == right_no:
                opcode = 'change'
                _left_line = left_line.replace('\0-', '').replace('\1', '')
                _right_line = right_line.replace('\0+', '').replace('\1', '')
                yield opcode, left_no, _left_line, right_no, _right_line
            elif right_line.startswith('\0+'):
                opcode = 'add'
                _right_line = right_line.replace('\0+', '').replace('\1', '')
                _left_line = ''
                yield opcode, left_no, _left_line, right_no, _right_line
            elif left_line.startswith('\0-'):
                opcode = 'delete'
                _left_line = left_line.replace('\0-', '').replace('\1', '')
                _right_line = ''
                yield opcode, left_no, _left_line, right_no, _right_line
        else:
            if left_no == right_no:
                opcode = 'equal'
                yield opcode, left_no, left_line, right_no, right_line
            else:
                opcode = 'move'
                yield opcode, left_no, left_line, right_no, right_line


def make_diff_table(diffs):
    template = '''  <tr>
      <td class="text-center">{}</td><td class="{}" {} nowrap="nowrap">{}</td>
      <td class="text-center">{}</td><td class="{}" {} nowrap="nowrap">{}</td>
    </tr>
    '''
    td_width = 'style="width:47%"'
    table = '    <table class="table table-bordered table-sm">\n'
    leftside_opcode = ('delete', 'move', 'equal', 'change')
    rightside_opcode = ('add', 'move', 'equal', 'change')
    for op_code, index_old, old_row, index_new, new_row in diffs:
        table += template.format(
            '' if not index_old else index_old,
            op_code if op_code in leftside_opcode else 'clear',
            td_width,
            '' if not old_row else html.escape(old_row).replace(' ', '&nbsp;'),
            '' if not index_new else index_new,
            op_code if op_code in rightside_opcode else 'clear',
            td_width,
            '' if not new_row else html.escape(new_row).replace(' ', '&nbsp;')
        )
    table += '</table>'
    return table


def htmldiff(original_text, modified_text):
    text_a = html.unescape(original_text)
    text_b = html.unescape(modified_text)
    diffs = get_diffs(text_a, text_b)
    diff_rows_gen = diff_formatter(diffs)
    return make_diff_table(diff_rows_gen)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print('Usage: python3 htmldiff.py <path/to/file1> <path/to/file2>')
        sys.exit(1)

    filename_a = sys.argv[1]
    filename_b = sys.argv[2]
    try:
        original_text = open(filename_a, 'r').read()
        modified_text = open(filename_b, 'r').read()
        diffs = get_diffs(original_text, modified_text)
        diffs_gen = diff_formatter(diffs)
        for diff in diffs_gen:
            print(
                "{!s:6} {!s:40} {!s:40}".format(
                    diff[0], (diff[1], diff[2]), (diff[3], diff[4]))
            )
    except Exception as err:
        print(err)
