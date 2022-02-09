set terminal pngcairo size 1480, 1920 font "Helvetica, 40"
set output outfile

set yrange [emin:emax]
set cbrange [0:1]
set xrange [0.05:0.2]
unset key
set grid lw 2
unset xtics

plot filename u 1:($2 - fermi):3 w l lw 8 lc palette
