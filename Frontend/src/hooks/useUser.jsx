import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";

export default function useUser() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initSession = async () => {
      const { data } = await supabase.auth.getSession();
      if (data.session) setUser(data.session.user);
      setLoading(false);
    };

    initSession();

    const { data: subscription } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => subscription?.subscription?.unsubscribe();
  }, []);

  const handleAuth = async (isSignup, email, password) => {
    const method = isSignup
      ? supabase.auth.signUp
      : supabase.auth.signInWithPassword;

    const { data, error } = await method({ email, password });

    if (error) {
      alert(error.message);
      return;
    }

    if (isSignup) {
      alert("Signup successful! Check your email for confirmation.");
    } else {
      setUser(data.user);
    }
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
    setUser(null);
  };

  return { user, handleAuth, handleLogout, loading };
}
