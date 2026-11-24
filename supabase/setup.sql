-- 드론경보 기기 연동용 테이블 (Supabase SQL Editor에 붙여 넣고 Run)
-- 방 코드(id)마다 한 행에 앱 상태 전체(가상 시연 데이터)를 저장합니다.
-- 공개 키(anon/publishable)로 읽고 쓰는 시연용 설정입니다. 실제 부대·인원 정보는 넣지 마세요.

create table if not exists public.drone_state (
  id          text primary key,
  rev         bigint      not null default 0,
  state       jsonb       not null,
  updated_at  timestamptz not null default now()
);

alter table public.drone_state enable row level security;

drop policy if exists "drone_state demo read"   on public.drone_state;
drop policy if exists "drone_state demo insert" on public.drone_state;
drop policy if exists "drone_state demo update" on public.drone_state;

create policy "drone_state demo read"   on public.drone_state for select to anon, authenticated using (true);
create policy "drone_state demo insert" on public.drone_state for insert to anon, authenticated with check (true);
create policy "drone_state demo update" on public.drone_state for update to anon, authenticated using (true) with check (true);

grant select, insert, update on public.drone_state to anon, authenticated;
