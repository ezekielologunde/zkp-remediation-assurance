#include "examples/ozks_simple/ozks.h"
#include "verify_wrapper.h"
#include <iostream>
#include <vector>
#include <fstream>
#include <stdexcept>
using namespace ozks;
int main(){
 ozks_simple::OZKS db;
 key_type key{std::byte{1},std::byte{1},std::byte{1}};
 key_type absent{std::byte{1},std::byte{1},std::byte{0}};
 payload_type payload{std::byte{1},std::byte{2}};
 db.insert(key,payload);db.flush();
 auto c=db.get_commitment();auto q=db.query(key);auto nq=db.query(absent);
 std::vector<uint8_t> cb,pb,nb;c.save(cb);q.save(pb);nq.save(nb);
 db.insert(absent,payload);db.flush();std::vector<uint8_t> newer;db.get_commitment().save(newer);
 auto run=[&](const char* name,const std::vector<uint8_t>& commitment,const std::vector<uint8_t>& proof,int expected,const key_type& expected_key){
  uint8_t extracted[64]{};size_t len=64;
  int r=ozks_verify_proof(commitment.data(),commitment.size(),proof.data(),proof.size(),extracted,&len);
  bool same=len==expected_key.size();if(same)for(size_t i=0;i<len;i++)same &= extracted[i]==std::to_integer<uint8_t>(expected_key[i]);
  std::cout<<name<<" result="<<r<<" expected="<<expected<<" key_match="<<same<<std::endl;
  if(r!=expected || !same)throw std::runtime_error("control failed");
 };
 run("member",cb,pb,0,key);run("nonmember",cb,nb,1,absent);run("stale_proof_new_commitment",newer,pb,2,key);
 for(auto item:std::vector<std::pair<const char*,std::vector<uint8_t>>>{{"commitment.bin",cb},{"member.bin",pb},{"nonmember.bin",nb},{"new-commitment.bin",newer}}){std::ofstream f(std::string("/out/")+item.first,std::ios::binary);f.write(reinterpret_cast<const char*>(item.second.data()),item.second.size());}
 std::cout<<"THREE_WRAPPER_CONTROLS_PASSED"<<std::endl;
}
