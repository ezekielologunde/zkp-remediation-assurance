use methods::{SBOM_VALIDATOR_ELF, SBOM_VALIDATOR_ID};
use risc0_zkvm::{default_prover, ExecutorEnv, InnerReceipt};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

#[derive(Serialize)]
struct Inputs { root_hash: [u8; 32] }
#[derive(Deserialize)]
struct Outputs { root_hash: [u8;32], banned_list_hash: [u8;32], compliant: bool }

fn main() -> Result<(), Box<dyn std::error::Error>> {
    assert_eq!(std::env::var("RISC0_DEV_MODE").unwrap(), "0");
    let path=std::env::args().nth(1).expect("fixture path required");
    let fixture: serde_json::Value=serde_json::from_slice(&std::fs::read(path)?)?;
    let root: [u8;32]=hex::decode(fixture["root"].as_str().unwrap())?.try_into().unwrap();
    let proofs=&fixture["merkle_proofs"];
    assert_eq!(proofs.as_array().unwrap().len(),2);
    let purls: Vec<&str>=proofs.as_array().unwrap().iter().map(|p|p["purl"].as_str().unwrap()).collect();
    let expected_hash: [u8;32]=Sha256::digest(serde_json::to_vec(&purls)?).into();
    let env=ExecutorEnv::builder().write(&serde_json::to_string(proofs)?)?.write(&Inputs{root_hash:root})?.build()?;
    let info=default_prover().prove(env,SBOM_VALIDATOR_ELF)?;
    let receipt=info.receipt;
    assert!(!matches!(&receipt.inner,InnerReceipt::Fake(_)),"Fake receipt forbidden");
    receipt.verify(SBOM_VALIDATOR_ID)?;
    let outputs: Outputs=receipt.journal.decode()?;
    assert_eq!(outputs.root_hash,root);
    assert_eq!(outputs.banned_list_hash,expected_hash);
    assert!(outputs.compliant);
    let mut wrong_id=SBOM_VALIDATOR_ID;wrong_id[0]^=1;
    assert!(receipt.verify(wrong_id).is_err());
    let mut altered=receipt.clone();altered.journal.bytes[0]^=1;
    assert!(altered.verify(SBOM_VALIDATOR_ID).is_err());
    std::fs::write("audit-receipt.json",serde_json::to_vec(&receipt)?)?;
    println!("{}",serde_json::json!({"real_receipt_verified":true,"wrong_image_rejected":true,"altered_journal_rejected":true,"root_matches":true,"banned_list_matches":true,"compliant":outputs.compliant,"image_id":SBOM_VALIDATOR_ID}));
    Ok(())
}
