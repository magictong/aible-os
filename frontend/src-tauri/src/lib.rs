use std::{
    fs::{self, OpenOptions},
    io::Write,
    net::TcpStream,
    path::PathBuf,
    process::{Command, Stdio},
    thread,
    time::Duration,
};

fn append_log(line: &str) {
    if let Ok(home) = std::env::var("HOME") {
        let path = format!("{}/aible-debug.log", home);
        if let Ok(mut f) = OpenOptions::new().create(true).append(true).open(path) {
            let _ = writeln!(f, "{}", line);
        }
    }
}

fn backend_is_listening() -> bool {
    TcpStream::connect("127.0.0.1:8765").is_ok()
}

fn home_log_path(name: &str) -> Option<PathBuf> {
    std::env::var("HOME").ok().map(|home| PathBuf::from(home).join(name))
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let home = std::env::var("HOME").unwrap_or_default();
            let _ = fs::write(format!("{}/aible-debug.log", home), "Aible OS startup");

            if backend_is_listening() {
                append_log("backend already listening on 8765");
                return Ok(());
            }

            let backend_path = match std::env::current_exe() {
                Ok(exe) => {
                    append_log(&format!("current_exe = {}", exe.display()));
                    match exe.parent() {
                        Some(dir) => dir.join("start-backend"),
                        None => {
                            append_log("current_exe has no parent directory");
                            return Ok(());
                        }
                    }
                }
                Err(e) => {
                    append_log(&format!("failed to resolve current_exe: {}", e));
                    return Ok(());
                }
            };

            append_log(&format!("attempting native command spawn: {}", backend_path.display()));

            let stdout = home_log_path("aible-backend.out.log")
                .and_then(|p| OpenOptions::new().create(true).append(true).open(p).ok())
                .map(Stdio::from)
                .unwrap_or(Stdio::null());
            let stderr = home_log_path("aible-backend.err.log")
                .and_then(|p| OpenOptions::new().create(true).append(true).open(p).ok())
                .map(Stdio::from)
                .unwrap_or(Stdio::null());

            match Command::new(&backend_path)
                .stdout(stdout)
                .stderr(stderr)
                .spawn()
            {
                Ok(child) => {
                    append_log(&format!("native spawn returned ok, pid={}", child.id()));
                    for i in 0..20 {
                        thread::sleep(Duration::from_millis(500));
                        if backend_is_listening() {
                            append_log(&format!("backend listening after {} checks", i + 1));
                            return Ok(());
                        }
                    }
                    append_log("native spawn succeeded but backend never started listening on 8765");
                }
                Err(e) => {
                    append_log(&format!("NATIVE SPAWN ERROR: {}", e));
                }
            }

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
