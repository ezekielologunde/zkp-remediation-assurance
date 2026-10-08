use std::path::PathBuf;
fn main(){
 cc::Build::new().cpp(true).flag("-std=c++17").include("/native").include("/native/build").file("cpp/verify_wrapper.cpp").compile("ozks_verify_wrapper");
 println!("cargo:rustc-link-search=native=/native/build/lib");
 println!("cargo:rustc-link-lib=static=ozks-1.6");
 println!("cargo:rustc-link-lib=dylib=PocoFoundation");
 println!("cargo:rustc-link-lib=dylib=stdc++");
 let bindings=bindgen::Builder::default().header("cpp/verify_wrapper.h").allowlist_function("ozks_verify_proof").generate().expect("bindings");
 bindings.write_to_file(PathBuf::from(std::env::var("OUT_DIR").unwrap()).join("bindings.rs")).unwrap();
}
