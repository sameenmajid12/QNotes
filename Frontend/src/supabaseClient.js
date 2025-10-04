import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = "https://rpwvpanvccswvhddxpdj.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJwd3ZwYW52Y2Nzd3ZoZGR4cGRqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1OTgyMTIsImV4cCI6MjA3NTE3NDIxMn0.lB08q1ctotUf6SZoLEL4ImtY9wHNFUpuWUiVyl6z52U";

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);