for this table there is 3 steps 
1.  create tbl_product_raw, where 
    this step will take payload data from the message in the topic. 
    so as an ilustration will be formed a stream whose column only has payload
2.  create tbl_product_clean, in this steps will be formed a stream, the data in 
    the payload in tbl_branch_raw will be taken, and it will be split into columns 
    and the results of this stream will also be stored in the kafka topic 'tbl_product_clean'
