import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const urlOrPath = z
  .string()
  .refine(
    (v) => v.startsWith('/') || /^https?:\/\//.test(v),
    { message: '必须是站内路径（以 / 开头）或 http(s) URL' }
  );

const projects = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    status: z.enum(['shipped', 'building', 'experiment', 'online']),
    category: z.enum(['desktop', 'data', 'ai', 'other']),
    summary: z.string().max(120),
    cover: z.string().optional(),
    tags: z.array(z.string()).default([]),
    startDate: z.coerce.date(),
    links: z
      .array(
        z.object({
          type: z.enum(['github', 'download', 'article', 'external', 'demo']),
          label: z.string(),
          url: urlOrPath,
        })
      )
      .default([]),
    featured: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

export const collections = { projects };
