import { DsqlSigner } from "@aws-sdk/dsql-signer";
import { awsCredentialsProvider } from "@vercel/functions/oidc";
import { config } from "dotenv";
import type { NodePgDatabase } from "drizzle-orm/node-postgres";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import * as schema from "./schema";

config();

let pool: Pool | null = null;
let db: NodePgDatabase<typeof schema> | null = null;
let cachedToken: { token: string; expiresAt: Date } | null = null;

export async function getToken() {
  const now = new Date();
  if (cachedToken && cachedToken.expiresAt > now) {
    return cachedToken.token;
  }
  let signer: DsqlSigner;
  if (process.env.NODE_ENV === undefined) {
    signer = new DsqlSigner({
      // biome-ignore lint/style/noNonNullAssertion: <explanation>
      hostname: process.env.DB_CLUSTER_ENDPOINT!,
      region: "us-east-1",
    });
  } else {
    signer = new DsqlSigner({
      // biome-ignore lint/style/noNonNullAssertion: <explanation>
      hostname: process.env.DB_CLUSTER_ENDPOINT!,
      region: "us-east-1",
      credentials: awsCredentialsProvider({
        // biome-ignore lint/style/noNonNullAssertion: <explanation>
        roleArn: process.env.AWS_ROLE_ARN!,
      }),
    });
  }

  const token = await signer.getDbConnectAdminAuthToken();

  // Token is valid for 15 minutes; set to 14 minutes to be safe
  const expiresAt = new Date(now.getTime() + 14 * 60 * 1000);
  cachedToken = { token, expiresAt };

  return token;
}

export async function getConnection() {
  const now = new Date();

  // Check if pool exists and token is still valid
  if (db && cachedToken && cachedToken.expiresAt > now) {
    return db;
  }

  // Token is expired or pool is null, recreate pool and db
  try {
    if (pool) {
      // Close the existing pool
      await pool.end();
      pool = null;
      db = null;
    }

    const token = await getToken();

    pool = new Pool({
      // biome-ignore lint/style/noNonNullAssertion: <explanation>
      host: process.env.DB_CLUSTER_ENDPOINT!,
      user: "admin",
      password: token,
      database: "postgres",
      port: 5432,
      ssl: true,
      max: 20,
    });
    db = drizzle(pool, { schema });
    return db;
  } catch (error) {
    console.error("Failed to create database connection:", error);
    throw error;
  }
}

export async function closeConnection() {
  if (pool) {
    await pool.end();
    pool = null;
    db = null;
  }
}
