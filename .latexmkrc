# authorindex package writes cited authors to aut.idx;
# chain makeindex after each xelatex pass to populate main.and
$xelatex = 'xelatex -interaction=nonstopmode %O %S && makeindex -q -o main.and aut.idx 2>/dev/null; true';
