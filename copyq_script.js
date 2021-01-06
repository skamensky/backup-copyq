tab('clipboard');
for(i=size(); i>0; --i){
  print('record number '+ i + '\n');
  var record = str(read("text/plain",i-1));
  if(record){
    print(record+'\n');
  }
}
