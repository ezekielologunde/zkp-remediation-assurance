use methods::SBOM_VALIDATOR_ID;
use risc0_zkvm::{Receipt, InnerReceipt};
use serde::Deserialize;
use sha2::{Digest, Sha256};
#[derive(Deserialize)]
struct Outputs { root_hash:[u8;32], banned_list_hash:[u8;32], compliant:bool }
fn accepts(r:&Receipt,id:[u32;8],root:[u8;32],policy:[u8;32],compliant:bool)->bool {
    if r.verify(id).is_err(){return false;}
    let o:Outputs=match r.journal.decode(){Ok(x)=>x,Err(_)=>return false};
    o.root_hash==root && o.banned_list_hash==policy && o.compliant==compliant
}
fn main()->Result<(),Box<dyn std::error::Error>> {
    assert_eq!(std::env::var("RISC0_DEV_MODE").unwrap(),"0");
    let r:Receipt=serde_json::from_slice(&std::fs::read("/receipt.json")?)?;
    assert!(!matches!(&r.inner,InnerReceipt::Fake(_)));
    let f:serde_json::Value=serde_json::from_slice(&std::fs::read("benchmark/data/merkleproofs/batch_proof_2.json")?)?;
    let root:[u8;32]=hex::decode(f["root"].as_str().unwrap())?.try_into().unwrap();
    let p:Vec<&str>=f["merkle_proofs"].as_array().unwrap().iter().map(|x|x["purl"].as_str().unwrap()).collect();
    let policy:[u8;32]=Sha256::digest(serde_json::to_vec(&p)?).into();
    let mut bad_root=root;bad_root[0]^=1;
    let mut bad_policy=policy;bad_policy[0]^=1;
    let mut bad_id=SBOM_VALIDATOR_ID;bad_id[0]^=1;
    let mut bad_receipt=r.clone();bad_receipt.journal.bytes[0]^=1;
    let cases=[("original",accepts(&r,SBOM_VALIDATOR_ID,root,policy,true),true),
    ("expected_root",accepts(&r,SBOM_VALIDATOR_ID,bad_root,policy,true),false),
    ("expected_policy",accepts(&r,SBOM_VALIDATOR_ID,root,bad_policy,true),false),
    ("expected_compliance",accepts(&r,SBOM_VALIDATOR_ID,root,policy,false),false),
    ("expected_image",accepts(&r,bad_id,root,policy,true),false),
    ("altered_journal",accepts(&bad_receipt,SBOM_VALIDATOR_ID,root,policy,true),false)];
    for (name,actual,expected) in cases { assert_eq!(actual,expected,"{}",name);println!("{}",serde_json::json!({"case":name,"accepted":actual,"expected":expected})); }
    Ok(())
}
