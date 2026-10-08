
fn scalar_hex(v:F<G1>)->String { let mut b=v.to_repr(); b.as_mut().reverse(); format!("0x{}",hex::encode(b)) }
fn main(){
 let mut dec=GzDecoder::new(File::open("/evidence/honest.proof.proof").unwrap());
 let mut b:ProofData=bincode::deserialize_from(&mut dec).unwrap();
 let pp:PublicParams<G1,G2,C1,C2>=bincode::deserialize_from(BufReader::new(File::open("/runtime/circuits/step.r1cs.pp").unwrap())).unwrap();
 let (_,vk)=MyCompressedSNARK::setup(&pp).unwrap();
 let (authenticated,_)=b.proof.verify(&vk,b.num_steps,b.z0_primary.clone(),b.z0_secondary.clone()).unwrap();
 assert_eq!(authenticated,b.zi_primary);
 let before=bincode::serialize(&b.proof).unwrap();
 std::fs::write("/out/original-core.bin",&before).unwrap();
 b.zi_primary[1]+=F::<G1>::from(1u64);
 let after=bincode::serialize(&b.proof).unwrap();assert_eq!(before,after);
 let (still_authenticated,_)=b.proof.verify(&vk,b.num_steps,b.z0_primary.clone(),b.z0_secondary.clone()).unwrap();
 assert_eq!(authenticated,still_authenticated);assert_ne!(still_authenticated,b.zi_primary);
 let mut enc=GzEncoder::new(File::create("/out/changed-metadata.proof").unwrap(),Compression::default());bincode::serialize_into(&mut enc,&b).unwrap();enc.finish().unwrap();
 std::fs::write("/out/changed-core.bin",after).unwrap();
 let result=json!({"original_metadata_matches_authenticated":true,"proof_bytes_unchanged":true,"changed_metadata_differs_authenticated":true,"authenticated":authenticated.iter().map(|v|scalar_hex(*v)).collect::<Vec<_>>(),"changed_metadata":b.zi_primary.iter().map(|v|scalar_hex(*v)).collect::<Vec<_>>()});
 println!("{}",result);std::fs::write("/out/probe.json",serde_json::to_vec_pretty(&result).unwrap()).unwrap();
}
