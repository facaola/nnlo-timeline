# gnuplot

set term pdfcairo enhanced lw 1.5 size 30cm,20cm font "helvetica,14"
set output 'timeline-info-2019-05.pdf'

print "hello"
system("./timeline-info.py")

# the following line's format is critical, because it is parsed
# by timeline-info.py in order to generate the colours for the
# lines that connect the points to the text.
#
# - The numbering must start at 0 and go up by 1
#
# - the number of colours specified must match the modulo divisor
#   used below
#
set palette model RGB defined ( 0 '#c00000', 1 '#00a000', 2 '#4040d0')
unset colorbox

set border 1
unset ytics
set xtics nomirror

set multiplot
set origin 0.0,0.3
set size 0.6

set format x '{/*1.9 %.0f}'
set xtics offset 0,-1
set mxtics 2
set yrange [0.8:2]
set xrange [2001:2020.5]
mod(a,b)=int(a - b*int(a/b) + 0.5)

load 'timeline-info.labels'
#plot 'timeline-info.points' u 1:2 w p pt 6 lc rgb 'black' t ''
plot 'timeline-info.points' u 1:2:(mod($3,3)) w p pt 6 palette t ''

unset multiplot

set output
