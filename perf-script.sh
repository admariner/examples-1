#!/bin/bash
reqs=`find . -name "requirements.txt"`
folders=()
for req in $reqs; do
  echo $req
  module=`dirname $req`
  if test -f "$module/setup.sh"; then
    echo "$module has setup. will be run"
    folders+=($module)
  fi
done

for folder in $folders; do
  cd $folder &&
  pip install -r requirements.txt && \
  bash setup.sh && \
  python app.py -t index > metrics.txt && \
  python app.py -t query >> metrics.txt && \
  cd ..
done

if test -f "performance.txt"; then
  rm performance.txt
fi

metrics=`find . -name "metrics.txt"`
for file_m in $metrics; do
  echo `dirname $file_m` >> performance.txt &&
  cat $file_m | grep "QPS: " | grep "takes" >> performance.txt
done