/**
 * Test Supabase Authentication
 * Run with: node scripts/test_supabase_auth.js
 */

const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: './frontend/.env.local' });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

console.log('='.repeat(60));
console.log('Supabase Authentication Test');
console.log('='.repeat(60));

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Missing Supabase credentials!');
  console.log('URL:', supabaseUrl ? '✅ Set' : '❌ Missing');
  console.log('Key:', supabaseKey ? '✅ Set' : '❌ Missing');
  process.exit(1);
}

console.log('✅ Supabase credentials found');
console.log('URL:', supabaseUrl.substring(0, 30) + '...');
console.log('Key:', supabaseKey.substring(0, 20) + '...');

const supabase = createClient(supabaseUrl, supabaseKey);

async function testAuth() {
  console.log('\n' + '='.repeat(60));
  console.log('Testing Authentication...');
  console.log('='.repeat(60));

  // Test 1: Check connection
  console.log('\n1. Testing Supabase connection...');
  try {
    const { data, error } = await supabase.from('sensors').select('count').limit(1);
    if (error && error.code !== 'PGRST116') { // PGRST116 is "no rows returned" which is OK
      console.error('❌ Connection error:', error.message);
    } else {
      console.log('✅ Supabase connection successful');
    }
  } catch (err) {
    console.error('❌ Connection failed:', err.message);
  }

  // Test 2: Try signup
  console.log('\n2. Testing Signup...');
  const testEmail = `test_${Date.now()}@example.com`;
  const testPassword = 'test123456';
  
  try {
    const { data, error } = await supabase.auth.signUp({
      email: testEmail,
      password: testPassword,
    });

    if (error) {
      console.error('❌ Signup error:', error.message);
      console.error('   Code:', error.status);
    } else {
      console.log('✅ Signup successful!');
      console.log('   User ID:', data.user?.id);
      console.log('   Email:', data.user?.email);
      console.log('   Session:', data.session ? 'Created' : 'Not created (email confirmation required)');
    }
  } catch (err) {
    console.error('❌ Signup failed:', err.message);
  }

  // Test 3: Check current session
  console.log('\n3. Checking current session...');
  try {
    const { data, error } = await supabase.auth.getSession();
    if (error) {
      console.error('❌ Session error:', error.message);
    } else {
      if (data.session) {
        console.log('✅ Active session found');
        console.log('   User:', data.session.user.email);
      } else {
        console.log('ℹ️  No active session');
      }
    }
  } catch (err) {
    console.error('❌ Session check failed:', err.message);
  }

  console.log('\n' + '='.repeat(60));
  console.log('Test Complete');
  console.log('='.repeat(60));
  console.log('\nNext Steps:');
  console.log('1. Check Supabase Dashboard → Authentication → Settings');
  console.log('2. Verify Site URL is set to: http://localhost:3000');
  console.log('3. Check if email confirmation is enabled/disabled');
  console.log('4. Check Redirect URLs include: http://localhost:3000/**');
}

testAuth().catch(console.error);

